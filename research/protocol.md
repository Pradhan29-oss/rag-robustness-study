# Experimental Protocol

Companion to `proposal.md`. Everything here is a fixed decision unless listed under "Open decisions".

## 0. Fixed components (all experiments)

| Component | Setting |
|---|---|
| Questions | 300 from RGB `en_refine.json` (Exp B: fixed random subset of 100, seed 42) |
| Embedding model | `sentence-transformers/all-MiniLM-L6-v2`, cosine similarity, normalized |
| BM25 | `rank-bm25` BM25Okapi, k1=1.5, b=0.75, lowercase, tokens = `\w+`, no stemming, no stop-word removal |
| Hybrid | Reciprocal Rank Fusion of BM25 and dense rankings, k=60, each over its top-100 |
| Vector store | Qdrant local/in-memory mode, exact (non-approximate) search, so ANN error is not a confound |
| Context size | Top K=5 passages, concatenated in rank order, same prompt template |
| Generator | One fixed model, temperature 0, max 256 new tokens (see open decisions) |
| Seeds | 42 for all sampling; recorded in every result file |
| Baseline | Closed-book (no passages), to expose parametric knowledge |
| Out of scope | Reranking, FastAPI, multiple generators, Chinese data |

## 1. Relevance labels

- Relevant set `Rel_q` = passages in q's RGB `positive` list that contain a gold alias (normalized substring). This drops 3 positives that have none.
- Distractor pool `D` = passages appearing only in `negative` lists (5,157 unique) and containing no gold alias of the question they are used for. This drops the 52 suspected false negatives.
- A passage that is positive for q and negative for q' keeps those labels per question (44 passages). It is never added to the distractor pool, because it is relevant to something.
- Normalization everywhere: lowercase, strip punctuation, collapse whitespace.
- Pooling bias: passages labelled neither positive nor negative for q (i.e. other questions' passages) count as non-relevant. Report this as a limitation.

## 2. Experiment A: retrieval robustness (core)

Noise enters **before indexing**. A separate index is built per corpus condition; every retriever sees the same corpus.

Base corpus `C0` = all unique positives of the 300 questions (about 2,440 passages).

| Condition | Corpus | Notes |
|---|---|---|
| Clean | `C0` | ρ = 0 |
| Distractor ρ=1/3, 2/3, 1 | `C0` + fraction ρ of `D` | Nested subsets (the 1/3 set is inside the 2/3 set), sampled once with seed 42. ρ=1 is the full pool. Report distractor share of corpus: roughly 0%, 41%, 58%, 68%. |
| Contradictory | `C0` + counterfactual passages (section 3) | ρ = 0, c = 2 counterfactual passages per question. |

Per question: retrieve top 10 (retrieval metrics at K=5 and 10); top 5 go to the generator. Run Clean, three Distractor levels and Contradictory for BM25, Dense, Hybrid: 5 conditions × 3 retrievers + closed-book.

Stretch (only if time): Contradictory + ρ=1 combined.

## 3. Contradiction generation and validation

Goal: a passage that makes a specific, checkable claim contradicting the gold answer, while the gold answer never changes.

Illustrative example (invented passage, not from the data): the original "Facebook acquired Instagram in 2012" becomes "Apple acquired Instagram in 2012". Gold stays "Facebook". Substitute `a'` = "Apple". RGB's own `en_fact.json` builds its wrong passages the same way (e.g. "Tampa, Florida" replaced by "Glendale, Arizona" with the rest of the sentence unchanged).

Rules:
1. Source passage: a positive of q that contains a gold alias (whole-token match).
2. Substitute `a'`: proposed automatically (seed 42) from gold answers of other questions with the same answer type (person, organization, place, number, date, other; type tagged heuristically then fixed by hand), then **approved or rewritten by hand** in `data/derived/substitutes.csv` (columns: qid, gold, substitute, type, approved). Dates and numbers keep the same format.
3. Edit: replace every alias occurrence of the gold answer in the passage with `a'` (longest alias first). Change nothing else.
4. Leak check (automatic, all passages): the counterfactual passage must contain `a'` and must contain no alias of the gold answer.
5. c = 2 counterfactual passages per question, built from two different positives, using the same `a'` (a consistent false claim).
6. Gold answers are stored once and never edited. Counterfactual passages carry `is_counterfactual=True`, `qid`, `source_passage`, `substitute`. They are never in `Rel_q`.
7. Multi-group questions (12): substitute only the first answer group; the question counts as contradicted on that group.
8. Manual validation: 50 random counterfactual passages are read by hand and scored on (a) really contradicts the gold answer, (b) reads fluently, (c) no new inconsistency introduced (e.g. leftover "2022" next to a substituted date). If more than 10% fail, revise the rules and regenerate. Report the pass rate in the paper.

Known risk: counterfactuals are lexically near-identical to their sources, so every retriever will rank them close to the original. That is a property of the construction. It makes this condition a test of whether the generator follows true vs false evidence more than a test of retriever discrimination. Say so in the paper.

## 4. Experiment B: generator robustness (supplementary)

Noise enters **after retrieval**, inside the final context. No retriever is involved, so Exp B cannot compare retrieval methods.

- 100 questions. Context = 5 passages, built from RGB's own lists, following `evalue.py` logic.
- Noise rate r ∈ {0, 0.4, 0.8}: fraction of the 5 passages taken from `negative`.
- Contradiction: 0 or 2 of the 5 positives replaced by their counterfactual versions (section 3).
- Passage order shuffled with seed 42, identical across conditions.
- Only generator metrics (section 5.2) are reported.

## 5. Metric definitions

### 5.1 Retrieval (Exp A; per question, macro-averaged over 300)

| Metric | Definition |
|---|---|
| Recall@K | `|Rel_q ∩ Top_K| / |Rel_q|`, K ∈ {5, 10}. Note `|Rel_q|` averages about 8, so Recall@5 cannot reach 1. |
| Hit@K | 1 if any relevant passage is in Top_K. Matters most, since one relevant passage suffices to answer. |
| MRR | 1 / rank of the first relevant passage (0 if none in top 10) |
| nDCG@K | Binary gain, log2 discount, ideal DCG from `min(|Rel_q|, K)` relevant items |
| CF@5 | Contradictory condition only: share of the top 5 that are counterfactual passages of q |

### 5.2 Answer quality (Exp A and B)

| Metric | Definition |
|---|---|
| Accuracy (primary) | Correct if, for every answer group, at least one alias appears in the normalized response. Modelled on RGB's alias-containment check; verify against `evalue.py` when porting. |
| Abstention rate | Response says the information is insufficient or gives no answer (regex list in `src/`, validated manually) |
| Wrong-context rate (WCR) | Contradictory condition: response contains a substitute `a'` and no gold alias. Fully automatic. |
| Other-wrong rate | Not correct, not abstention, not WCR |
| Token F1 / EM | Secondary. The prompt asks for a short answer; F1 and EM are computed against the best-matching alias after normalization. EM is reported for reference only, because generators often answer in sentences. |

Every response lands in exactly one class: correct, abstain, wrong-context, other-wrong.

Unsupported-claim rate (secondary, conditional): an LLM judge splits the response into atomic claims and labels each as supported or unsupported by the 5 provided passages. Rate = unsupported claims / total claims. Reported only if judge-vs-human agreement on the 100 manually labelled responses is at least 0.80; otherwise dropped and replaced by the automatic rates above. The judge model, prompt and version are recorded.

Robustness (RQ1, RQ2): relative degradation = `(metric_clean − metric_perturbed) / metric_clean`, plus absolute drop, per retriever. Mean over 300 questions with 95% bootstrap CIs (10,000 resamples, paired by question). Paired tests (McNemar for accuracy) between retrievers.

### 5.3 Manual validation

100 responses, stratified: 25 each from Clean, ρ=1, Contradictory and closed-book (one retriever). Labelled by hand into the four classes. Report agreement between automatic and manual labels. If a second annotator is available, report Cohen's kappa.

## 6. Latency measurement

- Hardware and software logged to `results/env.json`: CPU model, core count, RAM, GPU (if any), OS, Python, library versions.
- One process, batch size 1, no other heavy jobs running, fixed thread count.
- Stages timed separately with `time.perf_counter`: query embedding, BM25 scoring, vector search, RRF fusion, generation. Offline costs (index build, embedding time, index size on disk) reported separately.
- Warm-up: first 20 queries discarded (model load, caches).
- Repetitions: full query set run 3 times per condition; report median and p95 over all measured query-runs.
- Generation latency is reported but flagged: if the generator is an API, network variance dominates and it is not compared across hardware.

## 7. Token and cost accounting

- Per call, store prompt tokens, completion tokens, and context tokens (the 5 passages only) from the provider's usage field. For a local model, count with its own tokenizer.
- Cost = `prompt_tokens × price_in + completion_tokens × price_out`, with prices in `configs/pricing.yaml` stamped with the date checked. Local models: report tokens and wall-clock, API cost = 0, and say so.
- RQ3 compares retrieval quality (Hit@5, MRR), accuracy, retrieval latency and tokens across the three retrievers.

## 8. Open decisions (T to decide before Day 2 coding)

1. Generator model: a local open model (reproducible, free, needs a GPU or a small quantized model) vs an API model (needs key and budget; latency noisy). Pick one and freeze the version.
2. Substitute answers: fully manual for all 300 (about 1 hour) vs auto-proposed + manual approval (recommended).
3. Whether to run the stretch combined condition.
4. Second annotator for manual validation (supervisor or classmate).

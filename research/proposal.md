# Research Proposal

Version 2, revised 2026-11-09 after design review. Details live in `protocol.md` (exact definitions) and `dataset_audit.md` (what RGB actually contains).

## Title
Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts

## 1. Problem Statement
Retrieval-Augmented Generation (RAG) systems combine information retrieval with large language models to generate answers grounded in external knowledge.

Retrieved contexts can contain irrelevant, misleading or contradictory information, which can reduce answer reliability and cause unsupported claims. Prior benchmarks inject such noise at one fixed point and do not separate its effect on the retriever from its effect on the generator. This study separates the two.

## 2. Research Questions
- **RQ1:** How do BM25, dense and hybrid retrieval affect retrieval quality and answer correctness under increasing irrelevant-context levels?
- **RQ2:** How does contradictory evidence affect answer correctness and unsupported-claim rates across these retrieval strategies?
- **RQ3:** What trade-off exists between retrieval quality, answer reliability and computational cost?

## 3. Hypotheses
These are hypotheses; the results may reject them.
- **H1:** Retrieval quality (Hit@5, MRR) and answer accuracy decrease as the share of irrelevant passages in the corpus increases, and the rate of decrease differs between BM25 and dense retrieval.
- **H2:** Contradictory passages are retrieved at least as often as the true evidence they were derived from (they are near-duplicates of it), and raise the wrong-context answer rate for all three retrievers.
- **H3:** Hybrid retrieval costs more retrieval latency than either single method, and its gain in quality (if any) is smaller than the added cost.

## 4. Experimental Design

### 4.1 Where noise enters the pipeline

| Experiment | Where noise enters | What it can show | Priority |
|---|---|---|---|
| **A: Retrieval robustness** | Before indexing, inside the searchable corpus | Effect on retrieval and on downstream answers, per retriever | Core |
| **B: Generator robustness** | After retrieval, inside the final context | Effect on the generator only. Retriever cannot affect injected passages, so B cannot rank retrievers. | Supplementary |

### 4.2 Experiment A (core)
- Pooled corpus built from RGB passages. Clean corpus = all relevant passages; noise levels add 1/3, 2/3 and all of the irrelevant pool, giving a clean baseline plus three controlled noise levels.
- A separate contradictory condition adds two counterfactual passages per question (answer substituted, ground truth unchanged).
- Retrievers: BM25, dense (all-MiniLM-L6-v2), hybrid (RRF). Same top-5 context budget, prompt, generator and questions for all.
- Closed-book baseline for parametric knowledge.

### 4.3 Experiment B (supplementary)
- 100-question subset, 5-passage contexts built from RGB's labelled passages with noise rate in {0, 0.4, 0.8}, with and without 2 counterfactual passages.
- Reports generator metrics only.

### 4.4 Controlled across all runs
Generation model, prompt, question set, context budget (K=5), embedding model, seeds, hardware.

## 5. Dataset
RGB (Chen et al., AAAI-24), file `en_refine.json`, commit `65ec39e`: 300 English questions with per-question positive and negative passages. It has passage-level relevance labels but no shared corpus, so a pooled corpus is constructed. Full audit in `dataset_audit.md`.

## 6. Evaluation Metrics (summary)
- Retrieval: Recall@K, Hit@K, MRR, nDCG@K, counterfactual share of top-5.
- Answer: alias-containment accuracy (primary), abstention rate, wrong-context rate, other-wrong rate; token F1 and EM as secondary.
- Unsupported-claim rate: LLM-judged, reported only if it agrees with manual labels at 0.80 or higher.
- Robustness: relative and absolute degradation versus clean, with paired bootstrap CIs.
- Efficiency: per-stage latency (median, p95, warm-up and repetitions defined), token usage, estimated cost.
- A manually labelled sample of 100 responses validates the automatic scoring.

Exact formulas, procedures and validation rules are in `protocol.md`.

## 7. Scope for the Five-Day Sprint
In scope: three retrieval methods, one embedding model, one benchmark subset, three context conditions (clean, distractor, contradictory), three noise levels plus clean, one fixed generator, one reproducible experiment runner.

Out of scope (possible extensions): cross-encoder reranking, additional generators, CRAG or other datasets, Chinese data, API/UI layer.

## 8. Expected Contribution
A reproducible experimental framework that separates retrieval-side from generator-side noise and compares BM25, dense and hybrid retrieval under controlled irrelevant and contradictory contexts, with an analysis of reliability and cost.

A novelty claim will be made only after reading the full related-work sections of RGB, CRAG and the 2025 retrieval-robustness paper (see `literature_review.md`).

## 9. Limitations
- One small benchmark (300 questions, about 7.6k passages); results will not transfer automatically to web-scale corpora or other domains.
- Relevance labels are RGB's passage-level labels; unlabelled passages count as non-relevant (pooling bias).
- Counterfactual passages are synthetic and near-duplicates of real evidence; real conflicts are subtler.
- One generator and one embedding model.
- `en_refine.json` differs from the data in the AAAI-24 paper, so numbers are not directly comparable to the paper.
- Automatic scoring is imperfect; validated on a 100-response sample.
- Questions are news-based and may overlap with the generator's training data; the closed-book baseline measures this.

## 10. Reproducibility and Licensing
Code, configs, evaluation scripts and result files go in a public GitHub repository. Code is MIT. RGB data is CC BY-NC-SA 4.0, so it is not committed; a script downloads it, and any derived files that are shared carry the same license and cite RGB.

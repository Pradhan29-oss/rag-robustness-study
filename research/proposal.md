<<<<<<< HEAD
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
=======

# Research Proposal

## Title

Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts

## 1. Abstract

Retrieval-Augmented Generation (RAG) combines information retrieval with Large Language Models (LLMs) to produce answers grounded in external documents.

However, RAG systems may encounter irrelevant, misleading, or contradictory information during retrieval and generation.

This research investigates how sparse, dense, and hybrid retrieval strategies affect retrieval effectiveness, answer correctness, faithfulness, and computational efficiency under controlled noisy-context conditions.

The study distinguishes retrieval-side noise, introduced into the searchable document corpus, from context-side noise, introduced after retrieval and before generation.

The experiments will use a documented English subset of the Retrieval-Augmented Generation Benchmark (RGB), alongside controlled corpus construction and synthetic noise transformations where supported by the inspected dataset schema.

The objective is to develop a reproducible experimental framework and identify the reliability-cost trade-offs of different retrieval strategies.

## 2. Problem Statement

RAG systems depend on the quality of retrieved evidence.

In practical environments, retrieved information may contain:

- Irrelevant documents.
- Semantically similar but incorrect documents.
- Contradictory statements.
- Misleading evidence.
- Conflicting claims from multiple sources.

These conditions may reduce answer correctness and increase unsupported claims.

A further challenge is distinguishing failures caused by retrieval from failures caused by the generator's interpretation of retrieved evidence.

This study separates these failure sources through controlled experiments.

## 3. Research Gap

Existing research establishes several important limitations:

1. RGB evaluates noise robustness, negative rejection, information integration, and counterfactual robustness.
2. CRAG evaluates factual question answering across domains, question categories, and dynamic knowledge conditions.
3. Recent retrieval-robustness research studies whether RAG is better than non-RAG, the effect of retrieved document quantity, and document ordering.

These studies establish that imperfect retrieval and noisy evidence can influence RAG performance.

This project will investigate a focused experimental comparison of BM25, dense retrieval, and hybrid retrieval under separately controlled retrieval-side and context-side corruption.

The contribution is not claimed to be a new retrieval algorithm or the first study of RAG robustness.

The proposed contribution is an integrated, reproducible comparison of retrieval effectiveness, answer reliability, and computational cost under a clearly documented experimental design.

## 4. Research Questions

**RQ1 — Retrieval effectiveness**

How do BM25, dense retrieval, and hybrid retrieval differ in retrieval effectiveness and end-to-end answer quality?

**RQ2 — Noise robustness**

How do noise location (retrieval-side versus context-side), noise type (irrelevant versus contradictory), and noise severity affect answer correctness and faithfulness?

**RQ3 — Efficiency**

What trade-offs exist between answer quality, retrieval latency, generation latency, and token consumption across the three retrieval strategies?

## 5. Research Hypotheses

**H1:** Hybrid retrieval will outperform individual retrieval methods in retrieval effectiveness on the selected evaluation corpus.

**H2:** Increasing noise severity will reduce answer correctness and increase unsupported claims.

**H3:** Hybrid retrieval will exhibit a different quality-cost trade-off from BM25 and dense retrieval.

All hypotheses will be tested experimentally. No hypothesis is treated as a verified result.

## 6. Experimental Variables

### Independent Variables

- Retrieval strategy: BM25, Dense, Hybrid.
- Noise location: Retrieval-side, Context-side.
- Noise type: Irrelevant, Contradictory.
- Noise severity: Clean, Low, Medium, High.

### Dependent Variables

Retrieval:
- Precision@5
- Recall@5
- nDCG@5

Generation:
- Exact Match
- Token-level F1
- Answer correctness
- Unsupported-claim rate
- Faithfulness

Efficiency:
- Retrieval latency
- Generation latency
- Input token usage
- Output token usage

### Controlled Variables

- Same evaluation questions.
- Same document corpus for corresponding comparisons.
- Same top-K value: 5.
- Same embedding model.
- Same chunking configuration.
- Same generation model.
- Same generation prompt.
- Same decoding settings.
- Same context-token budget.
- Same evaluation procedure.
- Recorded hardware and software versions.

## 7. Dataset

### Primary Dataset

RGB: Retrieval-Augmented Generation Benchmark.

Repository:
https://github.com/chen700564/RGB

Research paper:
https://doi.org/10.1609/AAAI.V38I16.29728

### Initial Dataset Selection

- Language: English.
- Candidate file: en_refine.json.
- Initial target: 50 evaluation questions.
- Selection: stratified across available relevant categories, subject to schema verification.

The final subset size and category distribution will be recorded after inspecting the actual JSON files.

### Dataset Integrity

- Preserve original question IDs.
- Preserve original answers and evidence.
- Record dataset version and source.
- Do not silently modify original benchmark labels.
- Store derived data separately.
- Do not publish the original RGB files in this repository.

## 8. Experimental Methodology

### 8.1 System Architecture

1. Dataset loading.
2. Document normalization.
3. Chunking.
4. Index construction.
5. Retrieval.
6. Noise generation.
7. Context assembly.
8. Answer generation.
9. Evaluation.
10. Experiment logging.

### 8.2 Retrieval Baselines

| Method | Implementation |
|---|---|
| BM25 | rank-bm25 |
| Dense | Sentence Transformers + Qdrant |
| Hybrid | BM25 + dense retrieval + Reciprocal Rank Fusion |

Dense embedding model:

sentence-transformers/all-MiniLM-L6-v2

Top-K:

5

Hybrid fusion:

Reciprocal Rank Fusion (RRF), with a fixed and documented fusion constant.

### 8.3 Retrieval-Side Noise

Retrieval-side noise is introduced before indexing or retrieval.

Procedure:

1. Build the clean document corpus.
2. Add labeled irrelevant or contradictory documents.
3. Index the contaminated corpus.
4. Run the same evaluation questions.
5. Retrieve the top five passages.
6. Measure the actual noise proportion among retrieved passages.
7. Evaluate retrieval and answer quality.

The injected candidate-corpus proportion and the retrieved top-K noise proportion will be logged separately.

### 8.4 Context-Side Noise

Context-side noise is introduced after retrieval.

Procedure:

1. Retrieve evidence from the clean index.
2. Preserve the original relevant evidence.
3. Inject controlled irrelevant or contradictory passages.
4. Assemble the context.
5. Generate the answer.
6. Evaluate correctness and faithfulness.

### 8.5 Noise Conditions

For a context containing five passage slots:

| Condition | Noise slots |
|---|---:|
| Clean | 0 |
| Low | 1 |
| Medium | 2 |
| High | 3 |

For retrieval-side noise, the corpus contamination proportion is separately recorded.

### 8.6 Noise Generation and Labeling

Irrelevant passages:

- Select semantically unrelated passages.
- Avoid accidentally including supporting evidence.
- Record their original source and relevance label.

Contradictory passages:

- Start with an identifiable factual claim.
- Create a deliberately conflicting statement.
- Preserve the original evidence.
- Record the original claim, altered claim, source ID and contradiction label.
- Manually verify each generated contradiction.

Synthetic passages must never be presented as genuine benchmark documents.

## 9. Experimental Controls

| Parameter | Fixed setting |
|---|---|
| Initial questions | 50 |
| Retrieval top-K | 5 |
| Embedding model | all-MiniLM-L6-v2 |
| Generation model | gemini-3.8-flash |
| Temperature | 0 |
| Context budget | Maximum 2,000 retrieved-context tokens |
| Generation prompt | Version-controlled |
| Retrieval configuration | Version-controlled |
| Random seed | 42 |

The generation model is selected as a fixed experimental dependency, not as a claim that it is the best model. Its exact API availability and account access must be verified before the first run.

All runs will record the model identifier and date. Model changes require a separate experiment configuration.

## 10. Evaluation Metrics

### 10.1 Retrieval Metrics

**Precision@K**

Relevant retrieved passages divided by total retrieved passages.

**Recall@K**

Relevant retrieved passages divided by all known relevant passages.

**nDCG@K**

Measures ranking quality using graded relevance judgments and discounts lower-ranked results.

Use K=5 for the primary comparison.

### 10.2 Generation Metrics

**Exact Match (EM)**

Measures whether the normalized generated answer matches the reference answer.

**Token-level F1**

Measures token overlap between generated and reference answers.

EM and F1 will be used only where the answer format makes them meaningful.

**Unsupported-Claim Rate**

Number of unsupported factual claims divided by total factual claims.

**Faithfulness**

Proportion of factual claims supported by the provided evidence.

Abstentions and unanswerable questions will be evaluated separately from incorrect answers.

### 10.3 Efficiency Metrics

- Retrieval latency in milliseconds.
- Generation latency in milliseconds.
- Input tokens.
- Output tokens.
- Estimated API cost, if applicable.

Report averages and variability across repeated runs where feasible.

## 11. Manual Verification

A manually reviewed sample of generated answers will be selected.

Reviewers will assess:

1. Answer correctness.
2. Evidence support.
3. Contradiction handling.
4. Unsupported factual claims.
5. Appropriate abstention.

The review procedure and disagreements will be documented.

Where only one reviewer is available, results will be explicitly described as single-reviewer evaluation.

## 12. Technology Stack

- Python
- Sentence Transformers
- rank-bm25
- Qdrant
- Pandas
- Matplotlib
- PyYAML
- Pytest
- Gemini API

## 13. Expected Contributions

1. Reproducible RAG evaluation framework.
2. Controlled noise-generation methodology.
3. BM25, dense and hybrid retrieval baselines.
4. Retrieval-side versus context-side robustness comparison.
5. Reliability and computational-cost analysis.
6. Public implementation and research documentation.

## 14. Limitations

- Initial evaluation uses a limited English subset.
- RGB's published passages do not necessarily constitute a complete source corpus.
- Synthetic contradictions may not capture all real-world misinformation.
- One generator model limits generalization across LLMs.
- Automated faithfulness evaluation may be imperfect.
- API-based results may vary despite fixed decoding settings.

## 15. Research Integrity

No experimental findings will be fabricated.

All benchmark transformations will preserve traceability to the original samples.

All reported metrics must be reproducible from saved configurations and logs.

Dataset licensing and attribution must be respected.

## 16. Research Timeline

| Day | Work |
|---|---|
| Day 1 | Research design, dataset inspection, GitHub documentation |
| Day 2 | BM25, dense and hybrid baselines |
| Day 3 | Noise generation and experiments |
| Day 4 | Evaluation, manual review and results |
| Day 5 | Analysis, paper and portfolio documentation |

## 17. References

1. Chen, J., Lin, H., Han, X., & Sun, L. (2024). Benchmarking Large Language Models in Retrieval-Augmented Generation. AAAI 2024.
   https://doi.org/10.1609/AAAI.V38I16.29728

2. Yang, X. et al. (2024). CRAG: Comprehensive RAG Benchmark. NeurIPS 2024.
   https://arxiv.org/abs/2406.04744

3. Cao, S. et al. (2026). Evaluating the Retrieval Robustness of Large Language Models. COLM 2026.
   https://proceedings.colm.cc/paper_files/paper/2026/hash/b9c2e8a0bbed5fcfaf62856a3a719ada-Abstract-Conference.html
>>>>>>> b93f5757bcd811332d7edb43092a15ca2c653dcd

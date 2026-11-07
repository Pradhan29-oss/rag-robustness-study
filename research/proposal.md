
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

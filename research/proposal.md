
# Research Proposal

## Title

Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts

## 1. Abstract

Retrieval-Augmented Generation (RAG) improves Large Language Model (LLM) responses by retrieving external information before generating an answer. However, retrieved contexts may contain irrelevant, misleading, or contradictory information that can negatively affect answer reliability.

This research investigates how different retrieval strategies perform under controlled context noise. We compare sparse retrieval (BM25), dense retrieval, and hybrid retrieval under clean, irrelevant-distractor, and contradictory-context conditions.

The systems will be evaluated using retrieval quality, answer correctness, unsupported claims, response latency, and token consumption.

The objective is to identify which retrieval configuration offers the best balance between answer reliability and computational cost under imperfect retrieval conditions.

## 2. Problem Statement

RAG systems commonly assume that retrieved documents provide useful evidence. In practical applications, however, retrieved documents may contain:

- Irrelevant information.
- Semantically similar but incorrect information.
- Contradictory statements.
- Multiple documents with conflicting answers.

These conditions can cause LLMs to produce incorrect or unsupported answers.

The central problem is understanding how retrieval strategies influence the reliability of RAG systems when the supplied context contains controlled levels of irrelevant or contradictory information.

## 3. Research Questions

**Primary Research Question (RQ1):**

How do sparse, dense, and hybrid retrieval strategies affect RAG answer reliability under increasing levels of irrelevant and contradictory context?

**Secondary Research Questions:**

- RQ2: Which retrieval strategy maintains the highest answer accuracy under noisy-context conditions?
- RQ3: How does contradictory evidence affect unsupported claims and answer correctness?
- RQ4: What is the relationship between retrieval quality, answer reliability, latency, and token consumption?

## 4. Research Objectives

1. Implement three retrieval strategies: BM25, dense retrieval, and hybrid retrieval.
2. Develop a controlled evaluation dataset.
3. Introduce irrelevant and contradictory context at different noise levels.
4. Evaluate answer reliability under identical generation settings.
5. Compare retrieval and generation performance.
6. Measure computational cost and response latency.
7. Publish reproducible experiments and findings.

## 5. Research Hypotheses

**H1:** Hybrid retrieval will provide better retrieval quality than either BM25 or dense retrieval alone on the selected evaluation dataset.

**H2:** Increasing irrelevant context will reduce answer reliability for at least some retrieval configurations.

**H3:** Contradictory context will produce a greater reliability challenge than irrelevant context alone.

**H4:** Better retrieval quality will not necessarily guarantee better answer correctness when contradictory evidence is present.

These hypotheses will be tested experimentally. They are not assumed results.

## 6. Proposed Methodology

### 6.1 Experimental Setup

Build a reproducible RAG pipeline consisting of:

1. Document ingestion
2. Text preprocessing and chunking
3. Index construction
4. Retrieval
5. Controlled context manipulation
6. LLM-based answer generation
7. Evaluation and reporting

### 6.2 Retrieval Strategies

| Strategy | Implementation |
|---|---|
| Sparse | BM25 |
| Dense | Sentence Transformers embeddings |
| Hybrid | Reciprocal Rank Fusion (RRF) of sparse and dense results |

Dense embedding model: `sentence-transformers/all-MiniLM-L6-v2`

### 6.3 Context Conditions

| Condition | Description |
|---|---|
| Clean | Relevant evidence only |
| Distractor | Relevant evidence mixed with irrelevant passages |
| Contradictory | Relevant evidence mixed with deliberately conflicting passages |

### 6.4 Noise Levels

Use controlled levels of injected passages:

- Level 0: No injected passages.
- Level 1: 2 distractor passages.
- Level 2: 4 distractor passages.
- Level 3: 8 distractor passages.

For contradictory experiments, replace distractors with passages containing explicitly conflicting claims.

Keep the relevant evidence, generation prompt, model, and decoding settings fixed wherever possible.

Record context length and distinguish the effect of noise type from the effect of context length.

### 6.5 Dataset

Primary evaluation source:

RGB (Retrieval-Augmented Generation Benchmark).

The benchmark covers noise robustness, negative rejection, information integration, and counterfactual robustness.

Use a manageable, documented subset for the initial experiments.

Create controlled distractor and contradiction variants programmatically. Preserve the original questions, gold answers, and relevant evidence.

Optional external validation: CRAG benchmark, subject to dataset access and available time.

### 6.6 Evaluation Metrics

**Retrieval metrics**
- Recall@K
- Mean Reciprocal Rank (MRR)
- nDCG@K

**Generation metrics**
- Exact Match (EM)
- Token-level F1
- Answer correctness
- Unsupported claim rate
- Evidence-grounded answer rate

**Efficiency metrics**
- Average retrieval latency
- Average generation latency
- Input and output token consumption
- Estimated API cost, when applicable

### 6.7 Experimental Controls

To make the comparison fair:

- Use the same question set across retrieval strategies.
- Keep the generation model and prompt fixed.
- Fix temperature and decoding parameters.
- Keep the relevant evidence available across conditions.
- Record random seeds and dataset versions.
- Repeat stochastic experiments where feasible.
- Report failures and missing results rather than silently excluding them.

## 7. Expected Contributions

1. A reproducible experimental framework for evaluating RAG robustness.
2. A controlled dataset transformation pipeline for distractor and contradictory contexts.
3. A comparison of sparse, dense, and hybrid retrieval.
4. An empirical analysis of reliability versus computational cost.
5. Open-source code, configurations, and experimental results.

## 8. Limitations

- Initial experiments will use a limited dataset subset.
- Results may depend on the selected LLM and embedding model.
- API-based generation can introduce variability.
- Synthetic contradictory passages may not represent all real-world misinformation.
- Findings from this study should not be generalized to every RAG architecture.

## 9. Proposed Technology Stack

- Python
- Sentence Transformers
- BM25
- Qdrant
- Pandas
- Matplotlib
- PyYAML
- Pytest
- LLM API for answer generation

## 10. References

1. Chen et al. (2024), Benchmarking Large Language Models in Retrieval-Augmented Generation.
   https://doi.org/10.1609/aaai.v38i16.29728

2. Yang et al. (2024), CRAG: Comprehensive RAG Benchmark.
   https://arxiv.org/abs/2406.04744

3. Cao et al. (2026), Evaluating the Retrieval Robustness of Large Language Models.
   https://arxiv.org/abs/2505.21870

## 11. Research Timeline

| Day | Deliverable |
|---|---|
| Day 1 | Literature review, dataset and environment |
| Day 2 | Implement sparse and dense retrieval |
| Day 3 | Implement hybrid retrieval and noise injection |
| Day 4 | Run experiments and collect metrics |
| Day 5 | Analyze results, prepare visualizations and draft findings |

## 12. Research Integrity

No experimental results will be fabricated.

All numerical findings, performance comparisons, and conclusions will be based on actual executed experiments.

The final paper will distinguish measured results, hypotheses, limitations, and future work.

<<<<<<< HEAD
# Literature Review Notes

| Paper | Existing contribution | What we need to investigate |
|---|---|---|
| RGB 2024 (Chen et al., AAAI-24, arXiv:2309.01431) | RAG benchmark testing noise robustness, negative rejection, information integration, counterfactual robustness. English + Chinese; repo data audited in `dataset_audit.md`. Noise is injected into the final context. | Retrieval pipeline comparisons: noise placed in a searchable corpus so retrievers can differ |
| CRAG 2024 (Yang et al., arXiv:2406.04744) | Comprehensive RAG benchmark: 5 domains, 8 question categories, mock web and knowledge-graph APIs (README only read so far) | Dataset suitability for controlled perturbations; not inspected beyond the README |
| Retrieval Robustness 2025 (Cao et al., arXiv:2505.21870) | Studies RAG vs non-RAG, number of retrieved documents and document order across 11 LLMs (abstract only read so far) | Additional pipeline-level comparisons (BM25 vs dense vs hybrid) and contradictory evidence |

## Rules
- Do not write "no one has studied this" yet. Inspect the full papers and their related-work sections before any novelty claim.

## TODO
- [ ] Read full text and related work of arXiv:2505.21870
- [ ] Read the CRAG paper and `docs/dataset.md`
- [ ] Read RGB sections on noise construction and counterfactual evaluation
- [ ] Search for prior work comparing BM25, dense and hybrid retrieval under distractors and conflicting passages
- [ ] Search for knowledge-conflict work (e.g. context vs parametric knowledge) to cite in related work
=======

# Literature Review

## Research Topic

Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts.

## Paper 1: RGB Benchmark (2024)

**Title:** Benchmarking Large Language Models in Retrieval-Augmented Generation

**Authors:** Jiawei Chen, Hongyu Lin, Xianpei Han, Le Sun.

**Publication:** AAAI 2024.

**Paper:** https://doi.org/10.1609/aaai.v38i16.29728

### Research Objective

The paper investigates the fundamental capabilities required by LLMs in RAG systems.

It introduces four evaluation dimensions:

1. Noise robustness.
2. Negative rejection.
3. Information integration.
4. Counterfactual robustness.

### Key Findings

The authors demonstrate that LLMs can struggle with rejecting irrelevant or false information, integrating evidence, and handling counterfactual information.

### Limitations Relevant to Our Study

RGB primarily evaluates LLM capabilities across benchmark testbeds.

Our proposed work focuses on controlled comparisons of sparse, dense, and hybrid retrieval configurations under systematically manipulated context conditions.

### Research Gap

Further empirical investigation is needed into how retrieval strategy interacts with controlled distractor and contradiction levels when the generation model and relevant evidence are held constant.

---

## Paper 2: CRAG Benchmark (2024)

**Title:** CRAG – Comprehensive RAG Benchmark

**Authors:** Xiao Yang et al.

**Publication:** NeurIPS 2024, Datasets and Benchmarks Track.

**Paper:** https://arxiv.org/abs/2406.04744

**Official Repository:** https://github.com/facebookresearch/CRAG

### Research Objective

The authors introduce a comprehensive benchmark for evaluating factual question-answering systems using RAG.

### Dataset

CRAG contains:

- 4,409 question-answer pairs.
- Five domains.
- Eight question categories.
- Simulated web and knowledge graph APIs.

### Key Findings

The benchmark demonstrates that straightforward RAG implementations still struggle to provide consistently accurate and trustworthy answers.

### Limitations Relevant to Our Study

CRAG is designed for broad RAG evaluation across diverse tasks and knowledge conditions.

Our study instead isolates retrieval configurations and controlled distractor and contradictory-context conditions.

### Research Gap

A focused experimental comparison of retrieval methods under controlled noise conditions can complement broad benchmark evaluations and help identify reliability-cost trade-offs.

---

## Paper 3: Retrieval Robustness (2026)

**Title:** Evaluating the Retrieval Robustness of Large Language Models

**Authors:** Shuyang Cao, Karthik Radhakrishnan, David S. Rosenberg, Steven Lu, Pengxiang Cheng, Lu Wang, Shiyue Zhang.

**Publication:** Conference on Language Modeling (COLM), 2026.

**Paper:** https://arxiv.org/abs/2505.21870

### Research Objective

The authors investigate whether RAG consistently improves LLM performance and how retrieved document quantity and ordering influence answer quality.

### Research Questions

1. Is RAG always better than non-RAG?
2. Does retrieving more documents always improve performance?
3. Does document ordering influence model performance?

### Key Findings

The study reports that retrieval robustness varies across models and tasks. Imperfect robustness can prevent LLMs from fully benefiting from retrieved information.

### Limitations Relevant to Our Study

The paper investigates retrieval robustness through document availability, quantity, and ordering.

Our proposed study emphasizes controlled irrelevant and contradictory evidence while comparing multiple retrieval strategies.

### Research Gap

There is an opportunity to investigate the interaction between retrieval strategy, controlled evidence corruption, answer reliability, and computational cost.

---

## Comparative Literature Analysis

| Parameter | RGB | CRAG | Retrieval Robustness |
|---|---|---|---|
| Year | 2024 | 2024 | 2026 |
| Primary focus | LLM RAG capabilities | Broad RAG benchmark | Retrieval robustness |
| Noise robustness | Yes | Indirectly | Yes |
| Contradictory evidence | Counterfactual evaluation | False-premise questions | Imperfect retrieval |
| Document quantity | Not primary focus | Not primary focus | Yes |
| Document ordering | Not primary focus | Not primary focus | Yes |
| Retrieval strategy comparison | Not our primary focus | Not our primary focus | Not the main experimental axis |

## Identified Research Opportunity

Existing research establishes that noisy, irrelevant, and imperfectly retrieved evidence can affect RAG performance.

Our proposed study investigates a narrower experimental question:

How do sparse, dense, and hybrid retrieval strategies compare when exposed to controlled irrelevant and contradictory contexts?

The intended contribution is an empirical comparison with controlled experimental variables, reproducible configurations, and explicit reliability and efficiency measurements.

## Novelty Assessment

**Preliminary assessment: Incremental experimental contribution.**

This project does not claim to invent a new retrieval algorithm or establish the first study of RAG robustness.

Its contribution is the controlled experimental design, systematic comparison of retrieval strategies, and analysis of the relationship between context corruption, answer reliability, and computational cost.

A broader literature search will be required before claiming that the exact experimental combination has not been studied previously.

## References

1. Chen, J., Lin, H., Han, X., & Sun, L. (2024). Benchmarking Large Language Models in Retrieval-Augmented Generation. AAAI.
   https://doi.org/10.1609/aaai.v38i16.29728

2. Yang, X. et al. (2024). CRAG – Comprehensive RAG Benchmark. NeurIPS.
   https://arxiv.org/abs/2406.04744

3. Cao, S. et al. (2026). Evaluating the Retrieval Robustness of Large Language Models. COLM 2026.
   https://arxiv.org/abs/2505.21870
>>>>>>> b93f5757bcd811332d7edb43092a15ca2c653dcd

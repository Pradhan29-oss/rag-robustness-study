
# RAG Robustness Study

### Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![Research](https://img.shields.io/badge/Project-Experimental%20Research-purple)]()
[![Status](https://img.shields.io/badge/Status-In%20Progress-orange)]()

## Overview

This repository contains an experimental study investigating the robustness of Retrieval-Augmented Generation (RAG) systems under irrelevant and contradictory retrieval contexts.

The study compares three retrieval approaches:

- BM25 (Sparse Retrieval)
- Dense Semantic Retrieval
- Hybrid Retrieval (Reciprocal Rank Fusion)

The objective is to understand how retrieval strategies affect answer correctness, evidence grounding, and computational efficiency when retrieved contexts contain noise.

## Research Question

How do sparse, dense, and hybrid retrieval strategies affect RAG answer reliability under increasing levels of irrelevant and contradictory context?

## Research Objectives

1. Implement multiple retrieval strategies.
2. Construct controlled noisy-context evaluation conditions.
3. Evaluate answer reliability under identical generation settings.
4. Measure retrieval quality and computational efficiency.
5. Publish reproducible experimental results.

## Experimental Design

### Retrieval Methods

| Method | Description |
|---|---|
| BM25 | Keyword-based retrieval |
| Dense | Embedding-based semantic retrieval |
| Hybrid | Combination of sparse and dense retrieval |

### Evaluation Conditions

| Condition | Description |
|---|---|
| Clean | Relevant context only |
| Distractor | Relevant context plus irrelevant passages |
| Contradictory | Relevant context plus conflicting passages |

### Evaluation Metrics

- Recall@K
- MRR
- nDCG@K
- Exact Match
- Token-level F1
- Unsupported claim rate
- Retrieval latency
- Generation latency
- Token consumption

## Technology Stack

- Python
- Sentence Transformers
- Qdrant
- BM25
- Pandas
- Matplotlib
- PyYAML
- Pytest

## Repository Structure

```text
rag-robustness-study/
│
├── src/                    # Core implementation
├── configs/                # Experiment configurations
├── data/                   # Dataset and generated variants
├── experiments/            # Experiment execution scripts
├── results/                # Metrics and visualizations
├── research/
│   ├── proposal.md
│   └── literature_review.md
├── tests/                  # Automated tests
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/rag-robustness-study.git
cd rag-robustness-study
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Reproducibility

Experiments will use:

- Fixed dataset versions and documented subsets.
- Consistent question sets.
- Fixed retrieval parameters.
- Consistent LLM generation settings.
- Recorded random seeds.
- Saved experiment configurations.
- Versioned result files.

No results will be reported until experiments have actually been executed.

## Research Documentation

- [Research Proposal](research/proposal.md)
- [Literature Review](research/literature_review.md)

## Research References

1. [RGB Benchmark (AAAI 2024)](https://doi.org/10.1609/aaai.v38i16.29728)
2. [CRAG Benchmark (NeurIPS 2024)](https://arxiv.org/abs/2406.04744)
3. [Evaluating Retrieval Robustness (COLM 2026)](https://arxiv.org/abs/2505.21870)

## Project Status

Currently setting up the research environment and experimental framework.

Upcoming milestones:

- [ ] Dataset preparation
- [ ] BM25 implementation
- [ ] Dense retrieval implementation
- [ ] Hybrid retrieval implementation
- [ ] Controlled noise generation
- [ ] Experimental evaluation
- [ ] Results visualization
- [ ] Research paper preparation

## Research Integrity

This repository distinguishes between proposed hypotheses and experimentally verified findings.

All reported results will be based on reproducible experiments.

## License

License to be selected before public distribution of the implementation and any derived datasets.

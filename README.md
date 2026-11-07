
# RAG Robustness Study

**Evaluating the Robustness of Retrieval-Augmented Generation Systems Under Controlled Distractor and Contradictory Contexts**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Research](https://img.shields.io/badge/Research-Experimental-purple)
![Status](https://img.shields.io/badge/Status-In%20Progress-orange)
![License](https://img.shields.io/badge/Code-MIT-green)

## Overview

This project investigates the robustness of Retrieval-Augmented Generation (RAG) systems under irrelevant and contradictory retrieval contexts.

It compares three retrieval approaches:

- BM25 (Sparse Retrieval)
- Dense Semantic Retrieval
- Hybrid Retrieval (Reciprocal Rank Fusion)

The study distinguishes between retrieval-side noise and context-side noise to investigate how different failure sources influence RAG reliability.

## Research Questions

**RQ1 — Retrieval effectiveness**

How do BM25, dense retrieval, and hybrid retrieval differ in retrieval effectiveness and end-to-end answer quality?

**RQ2 — Noise robustness**

How do noise location (retrieval-side versus context-side), noise type (irrelevant versus contradictory), and noise severity affect answer correctness and faithfulness?

**RQ3 — Efficiency**

What trade-offs exist between answer quality, retrieval latency, generation latency, and token consumption across the three retrieval strategies?

## Research Hypotheses

- H1: Hybrid retrieval will outperform individual retrieval methods in retrieval effectiveness.
- H2: Increasing noise severity will reduce answer correctness and increase unsupported claims.
- H3: Hybrid retrieval will exhibit a different quality-cost trade-off from BM25 and dense retrieval.

These are hypotheses, not established results.

## Experimental Design

### Retrieval Methods

| Method | Implementation |
|---|---|
| BM25 | rank-bm25 |
| Dense | Sentence Transformers + Qdrant |
| Hybrid | BM25 + Dense + RRF |

### Noise Conditions

| Condition | Description |
|---|---|
| Clean | No injected noise |
| Low | 1 noisy passage out of 5 |
| Medium | 2 noisy passages out of 5 |
| High | 3 noisy passages out of 5 |

Two independent noise locations will be evaluated:

1. Retrieval-side: Noise is introduced into the searchable corpus before retrieval.
2. Context-side: Noise is introduced after retrieval and before generation.

Noise types:

- Irrelevant passages
- Contradictory passages

### Initial Experimental Configuration

| Parameter | Setting |
|---|---|
| Dataset | RGB English subset |
| Initial sample | 50 questions |
| Top-K | 5 |
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | Qdrant |
| Generation model | gemini-3.8-flash |
| Temperature | 0 |
| Context budget | 2,000 retrieved-context tokens |
| Random seed | 42 |

The dataset schema, sample composition and model availability will be verified before experiments begin.

## Evaluation Metrics

### Retrieval

- Precision@5
- Recall@5
- nDCG@5

### Generation

- Exact Match
- Token-level F1
- Answer correctness
- Unsupported-claim rate
- Faithfulness

### Efficiency

- Retrieval latency
- Generation latency
- Input token consumption
- Output token consumption
- Estimated API cost

## Repository Structure

```text
rag-robustness-study/
│
├── src/                    # Core RAG implementation
├── configs/                # Experiment configurations
├── data/                   # Local datasets and derived samples
├── experiments/            # Experiment execution
├── results/                # Generated metrics and charts
├── research/
│   ├── proposal.md
│   └── literature_review.md
├── tests/                  # Automated tests
│
├── README.md
├── requirements.txt
├── LICENSE
├── DATASET_LICENSE.md
└── .gitignore
```

## Installation

### 1. Clone

```bash
git clone https://github.com/Pradhan29-oss/rag-robustness-study.git
cd rag-robustness-study
```

### 2. Create virtual environment

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Dataset

Primary benchmark:

RGB — Retrieval-Augmented Generation Benchmark.

Repository:

https://github.com/chen700564/RGB

Research paper:

https://doi.org/10.1609/AAAI.V38I16.29728

The initial evaluation will use a documented English subset.

The original dataset will not be redistributed in this repository. Users must obtain it from the original source and comply with its license.

See [Dataset License and Attribution](DATASET_LICENSE.md).

## Reproducibility

Every experiment will record:

- Experiment ID
- Dataset version
- Dataset sample IDs
- Retrieval method
- Embedding model
- Generation model
- Top-K
- Noise type and severity
- Random seed
- Prompt version
- Retrieval and generation latency
- Token usage
- Evaluation metrics

Experiment configurations will be version-controlled.

Results will be published only after the corresponding experiments have actually run.

## Research Documentation

- [Research Proposal](research/proposal.md)
- [Literature Review](research/literature_review.md)
- [Dataset License and Attribution](DATASET_LICENSE.md)

## Project Status

### Research Design

- [x] Initial research proposal
- [x] Research questions
- [x] Hypotheses
- [x] Experimental variables
- [x] Noise taxonomy
- [ ] Dataset schema verification
- [ ] Dataset subset selection
- [ ] Dataset license documentation

### Implementation

- [ ] BM25 baseline
- [ ] Dense retrieval baseline
- [ ] Hybrid retrieval baseline
- [ ] Controlled noise generation
- [ ] Evaluation pipeline
- [ ] Experiment logging

### Results

- [ ] Retrieval evaluation
- [ ] Answer correctness evaluation
- [ ] Faithfulness evaluation
- [ ] Efficiency comparison
- [ ] Visualizations

## Research Integrity

This repository distinguishes between hypotheses, planned experiments and verified findings.

No performance improvements or research conclusions will be claimed without experimental evidence.

## Citation

If you use the RGB benchmark, cite:

Chen, J., Lin, H., Han, X., & Sun, L. (2024).

Benchmarking Large Language Models in Retrieval-Augmented Generation.

AAAI 2024.

https://doi.org/10.1609/AAAI.V38I16.29728

## License

Original implementation code: MIT License.

Third-party datasets, papers and external materials remain subject to their respective licenses.

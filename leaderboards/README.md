# 🏆 Protocol-Aware Leaderboards

> [!IMPORTANT]
> This directory is intentionally **conservative**. This repository will **not** publish a single global "SOTA" table across incompatible protocols.

| Result type | Meaning |
|---|---|
| ![official](https://img.shields.io/badge/official-1f6feb) | Released by a benchmark/challenge organizer |
| ![paper reported](https://img.shields.io/badge/paper%20reported-eaa221) | Copied from a published paper under a clearly identified protocol |
| ![reproduced](https://img.shields.io/badge/reproduced-2ea44f) | Independently reproduced using public code/checkpoint |

## 🔑 Leaderboard key

Each leaderboard is indexed by:

```text
dataset / split / direction / image-or-video / reranking
```

Examples:

```text
DetReIDX / official-test / A2G / video / no-reranking
CARGO / cross-view / A2G / image / no-reranking
```

> [!NOTE]
> No results are ranked here yet — `data/benchmarks.csv` currently contains only the schema header. Entries will be added as **official** or **reproduced** results become available under a fully specified protocol, with every row following the schema below.

## 📄 Raw schema

<details>
<summary><code>data/benchmarks.csv</code> — column reference</summary>

```csv
dataset,protocol,direction,method,backbone,rank1,map,reranking,result_type,source
```

| Column | Required | Meaning |
|---|---|---|
| `dataset` | ✓ | Dataset name matching `data/datasets.yaml` |
| `protocol` | ✓ | Exact split / protocol name |
| `direction` | ✓ | A2G, G2A, A2A, G2G, ALL, or benchmark-defined |
| `method` | ✓ | Method name matching `data/papers.yaml` where applicable |
| `backbone` | – | Backbone architecture |
| `rank1` | ✓ | Rank-1 accuracy |
| `map` | ✓ | Mean average precision |
| `reranking` | ✓ | `yes` / `no` |
| `result_type` | ✓ | `official`, `paper-reported`, or `reproduced` |
| `source` | ✓ | URL of the official result |

</details>

> [!TIP]
> Submit a result through the [benchmark result issue template](https://github.com/kailashhambarde/Aerial-Ground-Person-ReID/issues/new/choose) — see [CONTRIBUTING.md](../CONTRIBUTING.md) and the [Evaluation Guide](../docs/evaluation.md) for the full rules.

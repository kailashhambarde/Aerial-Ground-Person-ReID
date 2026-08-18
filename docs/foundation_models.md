# 🧠 Foundation-Model Baselines

A useful AG-ReID resource should include **training-free** and **light-adaptation** baselines rather than only task-specific supervised models.

## 🔁 Evaluation pipeline

```mermaid
flowchart LR
    IN["Crop & preprocess"] --> BB["Frozen backbone<br/>DINO · CLIP · SigLIP"]
    BB --> POOL["Pooling / CLS token"]
    POOL --> NORM["L2 normalize"]
    NORM --> SIM["Cosine similarity"]
    SIM --> RANK["Rank-1 / mAP"]

    classDef in fill:#eff6ff,stroke:#3b82f6,color:#1e3a8a;
    classDef out fill:#f0fdf4,stroke:#22c55e,color:#14532d;
    class IN in;
    class RANK out;
```

## 🧬 Proposed baseline families

| Family | Example evaluation |
|---|---|
| DINO | Global CLS / pooled patch embeddings + cosine similarity |
| CLIP | Image embeddings without text prompts |
| SigLIP | Direct image-image retrieval |
| Vision-language prompting | Identity-neutral semantic prompts |
| Self-supervised ViTs | Frozen backbone + retrieval head |

## 📋 Reporting rules

For training-free baselines, record:

- [ ] exact pretrained checkpoint
- [ ] image preprocessing
- [ ] crop policy
- [ ] feature token / pooling rule
- [ ] feature normalization
- [ ] similarity metric
- [ ] optional PCA / whitening
- [ ] optional re-ranking

> [!WARNING]
> A method is **not training-free** if any benchmark identity labels are used to optimize model parameters, prompts, adapters or metric heads.

## 🧪 Recommended evaluation matrix

Run each frozen backbone across:

| Dataset | Protocol notes |
|---|---|
| AG-ReID / AG-ReID.v2 | image, A2G + G2A |
| CARGO | synthetic, 5 aerial + 8 ground cameras |
| LAGPeR / G2APS-ReID | where accessible |
| DetReIDX | extreme distance, cross-session |
| AG-VPReID | frame or tracklet aggregation explicitly stated |
| WHU-MARS | modality/view subsets when permitted |

> [!NOTE]
> This section is intentionally **protocol-first**. Scores should be added only after reproducible scripts are available — until then, numbers belong in [leaderboards](../leaderboards/README.md), not here.

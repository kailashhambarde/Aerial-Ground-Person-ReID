# 🗃️ Datasets

> [!IMPORTANT]
> **Generated file — edit [`data/datasets.yaml`](../data/datasets.yaml), not this table.**
> Counts are tied to the linked source; verify the dataset version before using it in a paper.

**13 datasets catalogued** · **25,337 identities** · **3 video benchmarks** · **4 multimodal benchmarks**

| Dataset | Year | Category | IDs | Scale | Platforms | Modalities | Video | Geometry | Download |
| :------- | :---: | :-------- | ---: | :---- | :--------- | :--------- | :---: | :------- | :------- |
| [**AG-ReID**](https://arxiv.org/abs/2303.08597) | 2023 | Image.Person | 388 | 21,983 images | UAV, CCTV | RGB | — | alt. 15-45 m | [download](https://drive.google.com/file/d/1hzieEPlXfjkN3V3XWqI5rAwpF_sCF1K9/view) |
| [**AG-ReID.v2**](https://github.com/huynguyen792/AG-ReID.v2) | 2024 | Image.Person | 1,615 | 100,502 images | UAV, CCTV, wearable | RGB | — | alt. 15-45 m | [download](https://drive.google.com/drive/folders/16r7G_CuUqfWG6_UCT7goIGRMqJird6vK) |
| [**CARGO**](https://openaccess.thecvf.com/content/CVPR2024/html/Zhang_View-decoupled_Transformer_for_Person_Re-identification_under_Aerial-ground_Camera_Network_CVPR_2024_paper.html) | 2024 | Image.Person | 5,000 | 108,563 images | aerial-camera, ground-camera | RGB | — | — | [download](https://drive.google.com/file/d/1yDjyH0VtW7efxP3vgQjIqTx2oafCB67t/view) |
| [**AEA-FIRM**](https://ieeexplore.ieee.org/document/11072214) | 2025 | Text.Person | — | — | aerial, ground | RGB, text | — | — | [download](https://drive.google.com/file/d/1YYIpBDoJzTIwYRlpWUqEHmpo5GK05S_W/view) |
| [**AG-VPReID**](https://openaccess.thecvf.com/content/CVPR2025/html/Nguyen_AG-VPReID_A_Challenging_Large-Scale_Benchmark_for_Aerial-Ground_Video-based_Person_Re-Identification_CVPR_2025_paper.html) | 2025 | Video.Person | 6,632 | 32,321 tracklets; 9,600,000 frames | UAV, CCTV, wearable | RGB | ✓ | alt. 15-120 m | [download](https://drive.google.com/drive/folders/1wtdhKzK9Fbj7xkGAM84KNJ1uYCxSMHdj) |
| [**AG-VPReID.VIR**](https://arxiv.org/abs/2507.17995) | 2025 | Video.Person | 1,837 | 4,861 tracklets; 124,855 frames | UAV, CCTV | RGB, infrared | ✓ | — | [download](https://drive.google.com/drive/folders/1Iy814PqWjwIZcv6CZpieFju-Dop9Y2G7) |
| [**G2APS-ReID**](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_SeCap_Self-Calibrating_and_Adaptive_Prompts_for_Cross-view_Person_Re-Identification_in_CVPR_2025_paper.html) | 2025 | Image.Person | 2,788 | 200,800 images | UAV, CCTV | RGB | — | alt. 20-60 m | [download](https://pan.baidu.com/share/init?surl=MRrhqoQzwxw7qOx4Lqdl2g) |
| [**LAGPeR**](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_SeCap_Self-Calibrating_and_Adaptive_Prompts_for_Cross-view_Person_Re-Identification_in_CVPR_2025_paper.html) | 2025 | Image.Person | 4,231 | 63,841 images | aerial, ground | RGB | — | — | [download](https://pan.baidu.com/share/init?surl=MRrhqoQzwxw7qOx4Lqdl2g) |
| [**MP-ReID**](https://arxiv.org/pdf/2503.17096) | 2025 | Multimodal.Person | — | — | multi-platform | RGB, infrared | — | — | [download](https://drive.google.com/file/d/1hImLEMcsBB2kNV4McGyksVAumLjZQoUU/view) |
| [**CP2108**](https://ojs.aaai.org/index.php/AAAI/article/view/38339) | 2026 | Image.Person | — | — | aerial, ground | RGB | — | — | [download](https://github.com/ahu-xhao/SVPR-ReID) |
| [**DetReIDX**](https://www.it.ubi.pt/DetReIDX/) | 2026 | Video.Person | 509 | 12,600,000 boxes | UAV, DSLR, ground | RGB | ✓ | alt. 5.8-120 m; dist. 10-120 m | [download](https://github.com/kailashhambarde/DetReIDX/tree/main) |
| [**MOO**](https://github.com/TurtleSmoke/MOO) | 2026 | Image.Animal | — | — | — | RGB | — | — | [download](https://github.com/TurtleSmoke/MOO) |
| [**WHU-MARS**](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_WHU-MARS_A_Multispectral_Aerial-Ground_Benchmark_Towards_Any-Scenario_Person_Re-Identification_CVPR_2026_paper.html) | 2026 | Image.Person | 2,337 | 434,620 images | UAV, ground | RGB, NIR, TIR | — | — | — |

**Notes**

- **AEA-FIRM**: Text-based aerial pedestrian retrieval dataset introduced with AEA-FIRM.
- **AG-ReID**: 15 soft attributes per identity.
- **AG-ReID.v2**: 15 identity-level attributes; 807 train IDs and 808 test IDs.
- **AG-VPReID**: Large-scale video AG-ReID benchmark.
- **AG-VPReID.VIR**: Aerial-ground cross-modality video person ReID.
- **CARGO**: Synthetic Unity3D benchmark with 5 aerial and 8 ground cameras.
- **CP2108**: Large-scale text-aerial person retrieval benchmark introduced with SVPR-ReID.
- **DetReIDX**: Multi-session stress test; 18 UAV viewpoints; detection, tracking, ReID, search and action annotations.
- **G2APS-ReID**: Reconstructed from the G2APS person-search dataset.
- **LAGPeR**: Introduced with SeCap.
- **MOO**: Multi-view object observation dataset for animals, companion to 3D-LENS.
- **MP-ReID**: Multi-modal multi-platform person Re-ID benchmark and method.
- **WHU-MARS**: Any-scenario ReID benchmark spanning day/night, seasons and weather.

> [!TIP]
> Know a dataset that is missing or have corrections? Open a [paper issue](https://github.com/kailashhambarde/Aerial-Ground-Person-ReID/issues/new/choose) or follow [CONTRIBUTING.md](../CONTRIBUTING.md).


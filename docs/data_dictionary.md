# Data Dictionary

Reference for the Schurch 2020 CRC CODEX dataset and the pipeline's output schemas.

## Source

- **Citation:** Schurch CM, Bhate SS, Barlow GL, et al. *Cell* 182(5), 2020. DOI: [10.1016/j.cell.2020.07.005](https://doi.org/10.1016/j.cell.2020.07.005)
- **Access:** TCIA — [10.7937/TCIA.2020.FQN0-0326](https://doi.org/10.7937/TCIA.2020.FQN0-0326)
- **License:** see TCIA terms of use.

## Dataset shape

| Item | Value |
|---|---|
| Patients | 35 |
| Tissue regions (TMA spots) | 140 |
| Protein markers | 56 |
| Single cells | ~250,000 |
| Tissue type | FFPE colorectal cancer, invasive front |
| Modality | CODEX multiplexed immunofluorescence |
| Pixel size | TODO: confirm from acquisition metadata (Akoya CODEX standard: ~0.377 µm/px at 20x) |

## Marker panel

The full 56-marker panel is documented in Schurch 2020 Supplementary Table S1.
The current [`configs/default.yaml`](../configs/default.yaml) channel list is a
**12-marker stub** for development. Align it to the dataset metadata before
running on real data.

| Channel | Lineage / role | Notes |
|---|---|---|
| DAPI | Nuclear | Mesmer nuclear input |
| CD45 | Pan-immune | Mesmer membrane input (currently summed with PanCK) |
| CD4 | T helper | |
| CD8 | T cytotoxic | |
| CD20 | B cell | |
| CD68 | Macrophage | |
| CD163 | M2 macrophage | |
| PanCK | Epithelial | Tumor / epithelium |
| Vimentin | Stromal | |
| Ki67 | Proliferation | |
| αSMA | Smooth muscle / fibroblast | |
| CD31 | Endothelial | |
| TODO | TODO | Complete from Table S1 |

## Clinical groupings

- **CLR** — Crohn's-like reaction; tertiary lymphoid structures, better prognosis.
- **DII** — Diffuse inflammatory infiltration; worse prognosis.

These labels drive the comparative analyses in Stage 6.

## Cell-table schema

Per-spot tables are written by `extract_cell_features` to
`data/processed/cells_<spot>.parquet`.

| Column | Type | Description |
|---|---|---|
| `label` | int | Instance label, matches segmentation mask |
| `y`, `x` | float | Centroid in pixel coordinates (image origin = top-left) |
| `area` | float | Cell area in pixels |
| `<marker>` | float | Mean intensity per channel — one column per entry in `channels` |

## Excluded spots

Schurch 2020 flags a subset of TMA spots as excluded (low quality, segmentation
artifacts, etc.). Enumerate them here as they are confirmed.

| Spot ID | Reason |
|---|---|
| TODO | TODO |

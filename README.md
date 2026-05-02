# codex-crc-analysis

End-to-end analysis pipeline for CODEX multiplex immunofluorescence imaging of colorectal cancer tissue, built on the Schürch/Nolan CRC dataset. This pipeline covers the full workflow from raw multiplexed image data through cell segmentation, phenotyping, and spatial neighborhood analysis.

**Status: Active development: Summer 2026**

---

## Biological context

Colorectal cancer tumors are not uniform masses, as they contain spatially organized communities of cancer cells, immune cells, and stromal cells whose spatial relationships influence disease progression and treatment response. CODEX (Co-Detection by IndEXing) multiplexed immunofluorescence imaging allows simultaneous visualization of 50+ protein markers across intact tissue sections, enabling high-resolution mapping of the tumor microenvironment at single-cell resolution.

This project applies computational image analysis to characterize cellular composition and spatial architecture in CRC tissue, using a well-validated public dataset from Schürch et al. (2020).

---

## Dataset

**Source:** Schürch CM, Bhate SS, Barlow GL, et al. "Coordinated Cellular Neighborhoods Orchestrate Antitumoral Immunity at the Colorectal Cancer Invasive Front." *Cell* 182(5), 2020.  
**Access:** [STOmics Database / published supplementary data]  
**Contents:** CODEX imaging of 35 CRC patients, 140+ tissue regions, 56 protein markers, ~250,000 single cells

---

## Pipeline overview

```
Raw CODEX images (.tif)
        |
        v
1. Preprocessing
   - Background subtraction
   - Channel normalization
   - Tile stitching (if applicable)
        |
        v
2. Cell Segmentation  [Mesmer]
   - Nuclear + whole-cell segmentation
   - Instance mask generation
        |
        v
3. Feature Extraction
   - Per-cell marker intensity quantification
   - Morphological features
        |
        v
4. Cell Phenotyping
   - Marker-based gating / clustering (leiden)
   - Cell type annotation
   - UMAP visualization
        |
        v
5. Spatial Neighborhood Analysis  [Squidpy]
   - Spatial graph construction
   - Neighborhood enrichment analysis
   - Cellular community detection
        |
        v
6. Visualization & Reporting
   - Tissue maps colored by cell type
   - Neighborhood composition plots
   - Spatial statistics
```

---

## Repository structure

```
codex-crc-analysis/
│
├── data/
│   ├── raw/                  # Raw CODEX image tiles (.tif) — not tracked by git
│   ├── processed/            # Segmentation masks, cell tables — not tracked by git
│   └── README.md             # Data access and download instructions
│
├── notebooks/
│   ├── 01_preprocessing.ipynb
│   ├── 02_segmentation.ipynb
│   ├── 03_feature_extraction.ipynb
│   ├── 04_phenotyping.ipynb
│   ├── 05_spatial_analysis.ipynb
│   └── 06_visualization.ipynb
│
├── src/
│   ├── preprocess.py         # Image preprocessing utilities
│   ├── segment.py            # Mesmer segmentation wrapper
│   ├── phenotype.py          # Clustering and annotation helpers
│   └── spatial.py            # Squidpy analysis helpers
│
├── figures/                  # Output figures for README and reports
│
├── environment.yml           # Conda environment specification
├── .gitignore
└── README.md
```

---

## Environment setup

```bash
git clone https://github.com/Frankthetank7277/codex-crc-analysis.git
cd codex-crc-analysis
conda env create -f environment.yml
conda activate codex-crc
```

**Core dependencies:**

| Package | Purpose |
|---|---|
| `deepcell` | Mesmer cell segmentation |
| `squidpy` | Spatial analysis and neighborhood statistics |
| `cellpose` | Supplementary segmentation |
| `scanpy` | Single-cell data structures and clustering |
| `anndata` | Annotated data matrix format |
| `scikit-image` | Image preprocessing utilities |
| `pandas` / `numpy` | Data wrangling |
| `matplotlib` / `seaborn` | Visualization |

---

## Methods reference

- **Segmentation:** Mesmer (Greenwald et al., *Nature Biotechnology* 2022) — whole-cell segmentation using nuclear and membrane markers
- **Clustering:** Leiden algorithm via `scanpy` for unsupervised cell type discovery
- **Spatial analysis:** Squidpy neighborhood enrichment and spatial statistics (Palla et al., *Nature Methods* 2022)
- **Dataset:** Schürch et al., *Cell* 2020

---

## Results

*To be populated as pipeline development progresses (Summer 2026)*

---

## Author

Frank Lato · MS Bioengineering & Imaging Computing, UIUC  
[LinkedIn](https://www.linkedin.com/in/franklato/)

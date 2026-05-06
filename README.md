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
├── configs/
│   └── default.yaml             # Single source of truth for pipeline parameters
│
├── data/
│   ├── raw/                     # Raw CODEX image tiles (.tif) — not tracked by git
│   └── processed/               # Segmentation masks, cell tables — not tracked by git
│
├── notebooks/
│   └── 01_preprocessing_qc.ipynb   # End-to-end vertical slice (more added per stage)
│
├── src/codex_crc/               # Importable as `from codex_crc.<module> import ...`
│   ├── __init__.py
│   ├── io.py                    # Config loading, TIFF I/O, cell-feature extraction
│   ├── segmentation.py          # Mesmer wrapper (watershed fallback)
│   ├── phenotyping.py           # Arcsinh + Leiden clustering + annotation (stub)
│   ├── neighborhood.py          # Squidpy spatial neighborhoods (stub)
│   └── plotting.py              # Visualization helpers
│
├── tests/                       # Pytest suite (one test file per implemented module)
│   ├── test_io.py
│   ├── test_segmentation.py
│   └── test_plotting.py
│
├── results/                     # Output figures and tables — not tracked by git
│
├── pyproject.toml               # Package metadata + editable install
├── requirements.txt             # `-e .[dev]` for the pip path
├── environment.yml              # Conda environment specification (recommended)
├── CLAUDE.md                    # Project context for Claude Code sessions
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
pytest -q                                     # verify install
jupyter lab notebooks/01_preprocessing_qc.ipynb   # run the first vertical slice
```

The notebook generates a synthetic CODEX-like image when `data/raw/` is empty,
so the pipeline runs end-to-end before any real data is downloaded.

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

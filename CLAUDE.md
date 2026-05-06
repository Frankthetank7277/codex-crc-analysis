# CLAUDE.md — Project Context for Claude Code

This file is read by Claude Code at session startup. It provides persistent project context so every session starts with full awareness of the project's goals, conventions, and current status.

---

## What This Project Is

An end-to-end computational pathology / multiplex tissue imaging pipeline for colorectal cancer, built on the Schürch et al. 2020 CODEX dataset (Nolan lab, Stanford). The pipeline covers cell segmentation, phenotyping, and spatial neighborhood analysis of the tumor-immune microenvironment.

**This is a portfolio project** targeting R&D roles at companies like Tempus AI (Cell Imaging team), PathAI, Akoya Biosciences, 10x Genomics, and Vizgen. Every engineering decision should reflect that audience — clean, modular, well-documented code that a senior research engineer could inherit.

**GitHub repo:** <https://github.com/Frankthetank7277/codex-crc-analysis>

---

## Framing

Always use **computational pathology / multiplex tissue imaging** language rather than generic "spatial biology" or "machine learning." Specific terms that should appear naturally: multiplex immunofluorescence, tissue microarray, cellular neighborhood analysis, whole-slide image analysis, digital pathology, tumor microenvironment.

---

## Dataset

- **Source:** Schürch CM et al., *Cell* 182(5), 2020. DOI: 10.1016/j.cell.2020.07.005
- **Access:** TCIA — <https://doi.org/10.7937/TCIA.2020.FQN0-0326>
- **Contents:** 140 tissue regions, 35 CRC patients, 56 protein markers, ~250,000 single cells
- **Format:** CODEX multiplexed IF on FFPE tissue microarrays
- **Key clinical grouping:** CLR (Crohn's-like reaction) vs. DII (diffuse inflammatory infiltration)

---

## Pipeline Stages

1. Preprocessing & QC — `tifffile`, per-marker intensity histograms, spot flagging
2. Segmentation — Mesmer (primary), Cellpose (comparison sidebar)
3. Feature extraction — per-cell marker intensities → `cell_features.parquet`
4. Cell phenotyping — arcsinh transform, Leiden clustering, cell type annotation
5. Spatial neighborhood analysis — Squidpy, neighborhood enrichment, 9-CN replication
6. Biological interpretation — CLR vs. DII comparison, survival analysis, methodological novelty question

---

## Repository Structure

```
codex-crc-analysis/
├── README.md
├── CLAUDE.md               ← you are here
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── configs/
│   └── default.yaml        ← single source of truth for all parameters
├── data/
│   ├── raw/                ← source data, never modified
│   └── processed/          ← masks, cell tables, AnnData objects
├── docs/
│   ├── data_dictionary.md
│   ├── analysis_plan.md
│   └── checkpoints/
├── notebooks/              ← narrative notebooks, one per pipeline stage
├── results/                ← output figures and tables
├── src/                    ← all reusable logic lives here, not in notebooks
│   ├── __init__.py
│   ├── io.py
│   ├── segmentation.py
│   ├── phenotyping.py
│   ├── neighborhood.py
│   └── plotting.py
└── tests/
    └── test_io.py
```

---

## Engineering Conventions

- **Config-driven:** all parameters (marker lists, segmentation settings, clustering resolution, neighborhood radius) live in `configs/default.yaml`. No magic numbers in code.
- **Parquet for cell tables, zarr for image arrays.** Never rerun a 2-hour segmentation job because of a downstream bug.
- **Notebooks for narrative, `src/` for logic.** If a function is used more than once or will be used in production, it belongs in `src/`.
- **Type hints and docstrings on all public functions.**
- **One pytest test minimum per module.**
- **Commit every session**, even small progress.

---

## Biological Conventions

- Arcsinh transform with cofactor 5 is standard for CODEX marker intensities.
- Cell type annotation must be grounded in Schürch 2020 Supplementary Table S2 — do not invent thresholds.
- Any placeholder thresholds in `phenotyping.py` must be flagged with a TODO comment referencing Table S2.
- The target CN count is 9, replicating Schürch's result. The neighborhood radius default is 50 µm.
- Respect Schürch's flagged/excluded TMA spots — do not include them in analysis.

---

## Key Dependencies

| Package | Purpose |
|---|---|
| `deepcell` | Mesmer segmentation |
| `cellpose` | Comparison segmentation |
| `squidpy` | Spatial neighborhood analysis |
| `scanpy` / `anndata` | Single-cell data structures and clustering |
| `tifffile` | CODEX image loading |
| `scikit-image` | Image preprocessing |
| `pandas` / `numpy` | Data wrangling |
| `matplotlib` / `seaborn` | Visualization |
| `lifelines` | Survival analysis (Week 8) |

---

## Current Status

- [ ] Repo scaffolded
- [ ] README written
- [ ] `configs/default.yaml` populated
- [ ] `src/` modules stubbed
- [ ] First thin vertical slice working
- [ ] Data downloaded
- [ ] Segmentation running

Update this checklist at the start of each session.

---

## Owner

Frank Lato · MS Bioengineering & Imaging Computing, UIUC  
LinkedIn: <https://www.linkedin.com/in/franklato/>

# Analysis Plan

Living document. Captures pipeline stages, methodological decisions, evaluation
criteria, and open questions. Update at the end of each working session.

## Pipeline stages

| Stage | Goal | Output |
|---|---|---|
| 1. Preprocessing & QC | Load CODEX TIFFs, per-marker intensity histograms, flag low-quality spots | QC report, included/excluded spot list |
| 2. Segmentation | Mesmer whole-cell (primary), Cellpose comparison (sidebar) | `mask_<spot>.tif` per spot |
| 3. Feature extraction | Per-cell mean intensities + morphology | `cells_<spot>.parquet` |
| 4. Cell phenotyping | Arcsinh transform, Leiden clustering, type annotation grounded in Schurch Table S2 | AnnData with `cell_type` column |
| 5. Spatial neighborhood analysis | Squidpy graph (50 µm radius), 9-CN clustering replicating Schurch 2020 | AnnData with `neighborhood` column, CN composition table |
| 6. Biological interpretation | CLR vs DII comparison, survival analysis (`lifelines`), methodological novelty question | Figures, statistical tests, writeup |

## Methodological decisions

| Decision | Choice | Rationale |
|---|---|---|
| Segmentation backend | Mesmer | Whole-cell, validated on multiplex IF (Greenwald 2022) |
| Intensity transform | arcsinh, cofactor=5 | Standard for CODEX; equalizes signal across markers |
| Neighborhood radius | 50 µm | Schurch 2020 default |
| Target N_CN | 9 | Replicate Schurch 2020 result |
| Clustering | Leiden | Standard in scanpy ecosystem, deterministic with seed |
| Cell-type annotation | Marker thresholds from Schurch Table S2 | Grounded, reproducible — not invented |

## Evaluation criteria

- **Segmentation:** visual QC overlays on a held-out TMA spot; cell-count density vs. expected; Mesmer↔Cellpose IoU.
- **Phenotyping:** marker enrichment per Leiden cluster matches expected lineage from Table S2; UMAP shows separable lineages.
- **Neighborhood:** 9-CN composition and tissue-level distribution qualitatively match Schurch 2020 Figure 4.
- **Survival:** CN composition predicts CLR vs DII status with effect size comparable to Schurch 2020.

## Open questions

- Which TMA spots to exclude (track in `data_dictionary.md`).
- Membrane-channel composition for Mesmer — currently `PanCK + CD45`; revisit once panel is finalized.
- Cofactor sensitivity — does `cofactor=5` hold for this data subset, or does it warrant a per-marker tuning step?
- Methodological novelty angle — what does this work add beyond replicating Schurch 2020? (Candidate: CN robustness to segmentation choice, or alternative neighborhood graph constructions.)

## Status checkpoints

Per-stage checkpoint reports go in [`checkpoints/`](checkpoints/).

## Timeline

| Stage | Target | Status |
|---|---|---|
| 1–2 (preprocessing + segmentation) | TODO | Vertical slice working on synthetic data |
| 3–4 (features + phenotyping) | TODO | Stub |
| 5 (neighborhoods) | TODO | Stub |
| 6 (biology) | TODO | Not started |

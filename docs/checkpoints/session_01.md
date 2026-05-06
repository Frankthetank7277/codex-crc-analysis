# Session 01 — Inheriting-engineer review

**Date:** 2026-05-06
**Branch:** `claude/great-bohr-43c328`
**Commits reviewed:** `ba15933` (scaffold), `ff7c034` (docs)

Review framed as a senior research engineer inheriting the repository.

---

## 1. What's already strong

- **Real package layout, not "notebook with helpers."** `src/codex_crc/` + `pyproject.toml` editable install means imports work the same in notebooks, tests, and any future CLI. That's 50% of the battle in research code.
- **Config-driven, no magic numbers.** Every threshold either lives in `configs/default.yaml` or is flagged TODO with a Schürch Table S2 reference. A reviewer can see exactly what's grounded vs. provisional.
- **Slice runs end-to-end on commit one** via the synthetic-data fallback. Onboarding doesn't need 100 GB of imaging data; CI never will. Good pattern for research repos that usually require hours of setup.
- **Tests target behavior, not coverage theater.** `test_extract_cell_features_per_channel_intensity` actually checks per-channel correctness; `test_load_codex_tiff_channel_mismatch_raises` enforces a real invariant. Better than typical research pytest.
- **Mesmer-or-watershed fallback with identical return shape.** Heavy ML deps don't gate the rest of the pipeline, and the contract is symmetric so callers don't branch.
- **Living docs.** `analysis_plan.md` calls out open questions by name (cofactor sensitivity, CN robustness, novelty angle); most research repos never write this down.

## 2. Top three technical gaps

1. **TIFF loading is unverified against real CODEX data.** `load_codex_tiff` assumes a single multi-channel array. Real Schürch files are often OME-TIFF with one page per marker, or per-cycle subdirectories. `tifffile.imread` returns different shapes for those structures, and the channel-first heuristic could pick the wrong axis. Until this runs against an actual TMA spot, every downstream stage rests on an assumption.
2. **Mesmer path has never executed.** Only watershed is exercised in tests. The `image_mpp=0.377` is a guess, the membrane-channel sum (`PanCK + CD45`) is unmotivated, and Mesmer's input normalization expectations aren't verified. The fallback masks the risk — when this finally runs on real data, expect debugging.
3. **No data manifest, no batch entry point.** The notebook does `raw_dir.glob('*.tif*')` and picks index 0. That doesn't generalize to 140 spots × 35 patients × CLR/DII labels. There's no `spot_id → file → patient → group → excluded` mapping, no canonical excluded-spot list (just `TODO` in `data_dictionary.md`), and no script-mode runner. Stage 4 onward will hit this wall immediately.

**Honorable mentions** (not blocking but real): no CI, no `image_mpp` derivation from TIFF metadata, no preprocessing layer (background subtraction / normalization is in the README but not in code), only mean intensity per cell (no std/quantiles), Cellpose mentioned in README but no module exists.

## 3. Best next 2–3 steps

1. **Pull one real TMA spot from TCIA, get the loader right.** Inspect with `tifffile.TiffFile(path).pages[0].tags` to confirm storage layout. Derive `image_mpp` from the resolution tags rather than hardcoding. Update `configs/default.yaml` channel list against the actual 56-marker order. Run the full slice once, including `run_mesmer`. This single step retires gaps #1 and #2 simultaneously and gives the first real figure.
2. **Add the manifest layer.** A small `data/raw/manifest.csv` (spot_id, path, patient_id, group, excluded) plus `io.load_spot(manifest, spot_id)`. Then add `scripts/run_pipeline.py` that iterates the manifest and writes per-spot parquet. This is what stage 4 phenotyping needs as input.
3. **Add CI** (small, parallelizable with the above). One `.github/workflows/test.yml` that does `pip install -e .[dev] && pytest -q`, plus a `ruff` step. Tiny effort, but every future PR being green is what makes this look like a maintained project to a reviewer (and to the owner three months later).

If forced to pick just two: drop CI. Gaps #1 and #2 are blocking; CI is leverage for later.

## 4. Files that look too thin, too broad, or poorly named

| File | Issue | Suggested resolution |
|---|---|---|
| `src/codex_crc/io.py` | **Too broad.** Mixes config loading, TIFF I/O, and `extract_cell_features` (which is feature computation, not I/O). | Split into `io.py` (config + TIFF + parquet) and `features.py` (`extract_cell_features`). Move that test out of `test_io.py` accordingly. |
| `src/codex_crc/phenotyping.py` | **Too thin** — one function plus TODOs. Borderline OK as a stub. | Either prototype `leiden_cluster` even with a placeholder annotation step, or add a docstring banner saying "intentionally empty until real cell-table is available." |
| `src/codex_crc/neighborhood.py` | **TODO-only.** No functions at all. | Don't create the file until the first function exists, OR keep it but add a 2-line "what this module will export" docstring so reviewers don't read it as forgotten. |
| `notebooks/01_preprocessing_qc.ipynb` | **Misleadingly named.** Title says "preprocessing & QC" but it does preprocessing + segmentation + feature extraction + plotting — i.e., the whole pipeline. | Rename to `01_pipeline_smoke_test.ipynb` until split into the 6 stage notebooks the README promises. |
| `configs/default.yaml` | **Stub channel list buried in a comment.** Real reviewer won't notice it'll break on real data. | Move the "TODO: replace with full 56-marker panel" warning to the top of the file as a banner comment. |
| `tests/test_io.py` | **Misplaced test.** `test_extract_cell_features_per_channel_intensity` belongs in `test_features.py` if io is split. | Follow the io split. |
| `requirements.txt` | **Surprising contents.** A reviewer expecting pinned deps sees `-e .[dev]` and three lines of comments. | Either delete it (let `pyproject.toml` be the pip story) or generate a real `pip freeze` lockfile alongside. The current state is neither. |
| README mention of Cellpose comparison | **Promises code that doesn't exist.** | Drop the bullet until `cellpose.py` lands, or add a one-line stub module so the README isn't aspirational fiction. |

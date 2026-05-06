"""Tests for codex_crc.io."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import tifffile

from codex_crc.io import (
    extract_cell_features,
    load_codex_tiff,
    load_config,
    save_cells_parquet,
)


def test_load_config_round_trip(tmp_path: Path):
    cfg_path = tmp_path / "test.yaml"
    cfg_path.write_text("project:\n  random_seed: 7\nchannels:\n  - DAPI\n  - CD45\n")
    cfg = load_config(cfg_path)
    assert cfg["project"]["random_seed"] == 7
    assert cfg["channels"] == ["DAPI", "CD45"]


def test_load_codex_tiff_chw(tmp_path: Path):
    arr = np.random.default_rng(0).integers(0, 255, size=(4, 32, 32), dtype=np.uint16)
    p = tmp_path / "stack.tif"
    tifffile.imwrite(p, arr)
    image, names = load_codex_tiff(p, channel_names=["DAPI", "CD45", "CD8", "PanCK"])
    assert image.shape == (4, 32, 32)
    assert names == ["DAPI", "CD45", "CD8", "PanCK"]


def test_load_codex_tiff_channel_mismatch_raises(tmp_path: Path):
    arr = np.random.default_rng(0).integers(0, 255, size=(4, 32, 32), dtype=np.uint16)
    p = tmp_path / "stack.tif"
    tifffile.imwrite(p, arr)
    with pytest.raises(ValueError):
        load_codex_tiff(p, channel_names=["DAPI", "CD45"])


def test_extract_cell_features_per_channel_intensity():
    image = np.zeros((2, 10, 10), dtype=np.float32)
    image[0, 2:5, 2:5] = 100.0  # cell 1: bright in DAPI
    image[1, 6:9, 6:9] = 50.0   # cell 2: bright in CD45
    mask = np.zeros((10, 10), dtype=np.int32)
    mask[2:5, 2:5] = 1
    mask[6:9, 6:9] = 2

    df = extract_cell_features(image, mask, ["DAPI", "CD45"])
    assert len(df) == 2
    assert {"DAPI", "CD45", "x", "y", "area", "label"}.issubset(df.columns)

    cell1 = df.loc[df["label"] == 1].iloc[0]
    cell2 = df.loc[df["label"] == 2].iloc[0]
    assert cell1["DAPI"] == pytest.approx(100.0)
    assert cell1["CD45"] == pytest.approx(0.0)
    assert cell2["DAPI"] == pytest.approx(0.0)
    assert cell2["CD45"] == pytest.approx(50.0)


def test_save_cells_parquet_round_trip(tmp_path: Path):
    df = pd.DataFrame({"label": [1, 2], "x": [1.0, 2.0], "y": [3.0, 4.0]})
    p = tmp_path / "subdir" / "cells.parquet"
    save_cells_parquet(df, p)
    assert p.exists()
    pd.testing.assert_frame_equal(pd.read_parquet(p), df)

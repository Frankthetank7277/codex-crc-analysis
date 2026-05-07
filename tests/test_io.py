"""Tests for codex_crc.io."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import tifffile

from codex_crc.io import (
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


def test_save_cells_parquet_round_trip(tmp_path: Path):
    df = pd.DataFrame({"label": [1, 2], "x": [1.0, 2.0], "y": [3.0, 4.0]})
    p = tmp_path / "subdir" / "cells.parquet"
    save_cells_parquet(df, p)
    assert p.exists()
    pd.testing.assert_frame_equal(pd.read_parquet(p), df)

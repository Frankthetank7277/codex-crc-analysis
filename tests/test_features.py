"""Tests for codex_crc.features."""

import numpy as np
import pytest

from codex_crc.features import extract_cell_features


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

"""Tests for codex_crc.segmentation."""

import numpy as np

from codex_crc.segmentation import run_watershed


def test_run_watershed_separates_two_distant_blobs():
    image = np.zeros((1, 32, 32), dtype=np.float32)
    image[0, 5:10, 5:10] = 200.0
    image[0, 22:28, 22:28] = 200.0
    mask = run_watershed(image, ["DAPI"], "DAPI")
    n_objects = len(set(np.unique(mask)) - {0})
    assert n_objects >= 2

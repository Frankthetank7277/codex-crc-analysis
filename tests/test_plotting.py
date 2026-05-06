"""Tests for codex_crc.plotting."""

import matplotlib

matplotlib.use("Agg")  # non-interactive backend

import pandas as pd
import pytest

from codex_crc.plotting import plot_cells


def test_plot_cells_returns_figure():
    df = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [3.0, 4.0, 5.0], "DAPI": [10.0, 20.0, 30.0]})
    fig = plot_cells(df, color_by="DAPI")
    assert fig is not None
    fig.clf()


def test_plot_cells_unknown_column_raises():
    df = pd.DataFrame({"x": [1.0], "y": [2.0]})
    with pytest.raises(KeyError):
        plot_cells(df, color_by="NoSuchMarker")

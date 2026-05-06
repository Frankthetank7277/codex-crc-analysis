"""Cell phenotyping: arcsinh transform, Leiden clustering, cell-type annotation.

Stage 4 of the pipeline. Cell-type annotation thresholds and marker panels
must be grounded in Schurch 2020 Supplementary Table S2 — do not invent thresholds.
"""

from typing import Sequence

import numpy as np
import pandas as pd


def arcsinh_transform(
    df: pd.DataFrame,
    marker_cols: Sequence[str],
    cofactor: float = 5.0,
) -> pd.DataFrame:
    """Arcsinh-transform marker columns with the given cofactor (CODEX standard: 5)."""
    out = df.copy()
    out[list(marker_cols)] = np.arcsinh(out[list(marker_cols)].to_numpy() / cofactor)
    return out


# TODO: leiden_cluster(df, marker_cols, resolution) -> labels
# TODO: annotate_cell_types(df, cluster_col, panel_table_s2) -> labels

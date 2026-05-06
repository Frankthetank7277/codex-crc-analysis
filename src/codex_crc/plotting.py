"""Plotting utilities for CODEX analysis."""

from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd


def plot_cells(
    df: pd.DataFrame,
    color_by: str,
    title: Optional[str] = None,
    save_path: Optional[str | Path] = None,
    point_size: float = 2.0,
    cmap: str = "viridis",
) -> plt.Figure:
    """Scatter cell centroids colored by a marker or label column. Returns the Figure."""
    if color_by not in df.columns:
        raise KeyError(f"color_by={color_by!r} not in DataFrame columns")
    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter(df["x"], df["y"], c=df[color_by], s=point_size, cmap=cmap)
    ax.invert_yaxis()  # image-coordinate origin is top-left
    ax.set_aspect("equal")
    ax.set_xlabel("x (px)")
    ax.set_ylabel("y (px)")
    ax.set_title(title or f"Cells colored by {color_by}")
    fig.colorbar(scatter, ax=ax, label=color_by)
    if save_path is not None:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig

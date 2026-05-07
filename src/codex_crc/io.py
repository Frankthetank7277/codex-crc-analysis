"""I/O utilities: config loading, CODEX TIFF loading, cell-table persistence."""

from pathlib import Path
from typing import Sequence, Tuple

import numpy as np
import pandas as pd
import tifffile
import yaml


def load_config(path: str | Path) -> dict:
    """Load a YAML config file and return as a dict."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def load_codex_tiff(
    path: str | Path,
    channel_names: Sequence[str] | None = None,
) -> Tuple[np.ndarray, list[str]]:
    """Load a multi-channel CODEX TIFF and return (image, channel_names).

    Image is normalized to (C, H, W). If channel_names is provided, it must match
    the channel count exactly.
    """
    image = tifffile.imread(str(path))
    if image.ndim == 2:
        image = image[np.newaxis, :, :]
    elif image.ndim == 3:
        # Heuristic: channel-first if first dim is the smallest of the three.
        if image.shape[0] > image.shape[-1] and image.shape[0] > image.shape[-2]:
            image = np.transpose(image, (2, 0, 1))
    else:
        raise ValueError(f"Unexpected image shape {image.shape}")

    n_channels = image.shape[0]
    if channel_names is None:
        names = [f"ch{i}" for i in range(n_channels)]
    else:
        names = list(channel_names)
        if len(names) != n_channels:
            raise ValueError(
                f"Channel count mismatch: image has {n_channels}, names has {len(names)}"
            )
    return image, names


def save_cells_parquet(df: pd.DataFrame, path: str | Path) -> None:
    """Persist a cell-features DataFrame as parquet, creating parent dirs as needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

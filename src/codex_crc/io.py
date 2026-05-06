"""I/O utilities: config loading, CODEX TIFF loading, cell-table extraction."""

from pathlib import Path
from typing import Sequence, Tuple

import numpy as np
import pandas as pd
import tifffile
import yaml
from skimage.measure import regionprops_table


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


def extract_cell_features(
    image: np.ndarray,
    mask: np.ndarray,
    channel_names: Sequence[str],
) -> pd.DataFrame:
    """Compute mean intensity per channel + centroid + area for each labeled cell."""
    if image.ndim != 3:
        raise ValueError(f"image must be (C, H, W); got shape {image.shape}")
    if image.shape[1:] != mask.shape:
        raise ValueError(
            f"image spatial shape {image.shape[1:]} != mask shape {mask.shape}"
        )
    if len(channel_names) != image.shape[0]:
        raise ValueError(
            f"channel_names length {len(channel_names)} != image channels {image.shape[0]}"
        )

    # regionprops_table accepts (H, W, C) intensity images and returns
    # mean_intensity-{i} columns, one per channel.
    intensity_hwc = np.transpose(image, (1, 2, 0))
    props = regionprops_table(
        mask,
        intensity_image=intensity_hwc,
        properties=("label", "centroid", "area", "mean_intensity"),
    )
    df = pd.DataFrame(props)
    rename_map = {f"mean_intensity-{i}": ch for i, ch in enumerate(channel_names)}
    df = df.rename(columns=rename_map)
    df = df.rename(columns={"centroid-0": "y", "centroid-1": "x"})
    return df


def save_cells_parquet(df: pd.DataFrame, path: str | Path) -> None:
    """Persist a cell-features DataFrame as parquet, creating parent dirs as needed."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)

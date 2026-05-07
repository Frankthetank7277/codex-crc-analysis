"""Per-cell feature extraction from segmentation masks and multi-channel images."""

from typing import Sequence

import numpy as np
import pandas as pd
from skimage.measure import regionprops_table


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

"""Cell segmentation wrappers (Mesmer primary, watershed fallback)."""

from typing import Sequence

import numpy as np
from scipy import ndimage as ndi
from skimage import filters, morphology
from skimage import segmentation as ski_seg
from skimage.feature import peak_local_max
from skimage.measure import label


def _channel_index(channel_names: Sequence[str], name: str) -> int:
    names = list(channel_names)
    if name not in names:
        raise ValueError(f"Channel '{name}' not found in {names}")
    return names.index(name)


def run_watershed(
    image: np.ndarray,
    channel_names: Sequence[str],
    nuclear_channel: str,
    min_cell_size: int = 20,
    peak_min_distance: int = 5,
) -> np.ndarray:
    """Watershed segmentation on the nuclear channel (Mesmer-free fallback)."""
    nuc = image[_channel_index(channel_names, nuclear_channel)].astype(np.float32)
    smoothed = filters.gaussian(nuc, sigma=1.0)
    threshold = filters.threshold_otsu(smoothed)
    binary = smoothed > threshold
    binary = morphology.remove_small_objects(binary, min_size=min_cell_size)
    distance = ndi.distance_transform_edt(binary)
    coords = peak_local_max(distance, min_distance=peak_min_distance, labels=binary)
    seeds = np.zeros(distance.shape, dtype=bool)
    if len(coords) > 0:
        seeds[tuple(coords.T)] = True
    markers = label(seeds)
    mask = ski_seg.watershed(-distance, markers, mask=binary)
    return mask.astype(np.int32)


def run_mesmer(
    image: np.ndarray,
    channel_names: Sequence[str],
    nuclear_channel: str,
    membrane_channels: Sequence[str],
    image_mpp: float = 0.377,
) -> np.ndarray:
    """Mesmer whole-cell segmentation; falls back to watershed if deepcell is unavailable."""
    try:
        from deepcell.applications import Mesmer
    except ImportError:
        return run_watershed(image, channel_names, nuclear_channel)

    nuc_idx = _channel_index(channel_names, nuclear_channel)
    mem_indices = [_channel_index(channel_names, c) for c in membrane_channels]
    nuc = image[nuc_idx].astype(np.float32)
    mem = image[mem_indices].sum(axis=0).astype(np.float32)
    stacked = np.stack([nuc, mem], axis=-1)[np.newaxis, ...]  # (1, H, W, 2)

    app = Mesmer()
    mask = app.predict(stacked, image_mpp=image_mpp, compartment="whole-cell")
    return mask[0, ..., 0].astype(np.int32)

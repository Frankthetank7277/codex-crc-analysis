"""Spatial neighborhood analysis (Squidpy). Replicates the 9-CN result of Schurch 2020.

Stage 5 of the pipeline. Implemented after phenotyping produces an AnnData
with cell-type labels and spatial coordinates.

Will export: `build_spatial_graph` (radius-based KNN over cell centroids),
`compute_cellular_neighborhoods` (k-NN composition vectors -> KMeans clustering
into N CNs), and `neighborhood_enrichment` (Squidpy permutation test for
cell-type co-occurrence within CNs).
"""

# TODO: build_spatial_graph(adata, radius_um, image_mpp) -> adata
# TODO: compute_cellular_neighborhoods(adata, k_neighbors, n_clusters) -> adata
# TODO: neighborhood_enrichment(adata) -> stats

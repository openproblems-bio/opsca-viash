# Datasets

Viash component for preparing data **before** running data integration methods.

## API

### Requires

* `adata.X`: raw counts
* batch label in `adata.obs` that is specified as a parameter to the script
* cell identity label in `adata.obs` that is specified as a parameter to the script

### Returns

This module creates Anndata objects that contain:

* `adata.uns['name']`: name of the dataset
* `adata.obs['batch']`: batch covariate
* `adata.obs['label']`: cell identity label
* `adata.var['highly_variable']`: label whether a gene is identified as highly variable
* `adata.layers['counts']`: raw, integer UMI count data
* `adata.layers['logcounts']`: log-normalized count data
* `adata.layers['logcounts_scaled']`: log-normalized count data scaled to unit variance and zero mean
* `adata.X`: same as in `adata.layers['logcounts']`

And transformations of the data:

* `adata.obsm['X_pca']`: PCA embedding of the log-normalized counts
* `adata.uns['uni']`: neighbors data generated by `scanpy.pp.neighbors()`
* `adata.obsp['pca_connectivities']`: connectivity matrix generated by `scanpy.pp.neighbors()`
* `adata.obsp['pca_distances']`: distance matrix generated by `scanpy.pp.neighbors()`
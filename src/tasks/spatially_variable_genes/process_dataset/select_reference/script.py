import anndata as ad
import squidpy as sq

### VIASH START
### VIASH END

print(">> Load data", flush=True)
adata = ad.read_h5ad(par['input'])

print(">> Look for layer", flush=True)
layer = adata.X if not par['input_layer'] else adata.layers[par['input_layer']]

print(">> Run SVG", flush=True)
sq.gr.spatial_neighbors(adata, coord_type="grid", delaunay=False)
sq.gr.spatial_autocorr(adata, 
                       layer="normalized",
                       mode="moran", 
                       n_perms=100, n_jobs=10, 
                       genes=adata.var_names)

n_svgs = par['num_features']
sel_genes = (
    adata.uns["moranI"]["I"].sort_values(ascending=False).head(n_svgs).index.tolist()
)

adata = adata[:, sel_genes]

print(">> Writing data", flush=True)
adata.write_h5ad(par['output'])

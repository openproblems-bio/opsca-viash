import anndata as ad
import squidpy as sq

# VIASH START
par = {
    'input_data': 'resources_test/spatially_variable_genes/10x_visium_mouse_brain/input_data.h5ad',
    'output': 'output.h5ad',
    'coord_type': 'grid',
    'max_neighs': 6,
}
meta = {
    'functionality_name': 'Sepal'
}
# VIASH END

print('Generate predictions', flush=True)
adata = ad.read_h5ad(par['input_data'])

sq.gr.spatial_neighbors(adata,
                        coord_type=par['coord_type'],
                        delaunay=False)

sq.gr.sepal(adata, 
            layer='counts',
            max_neighs=par['max_neighs'], 
            genes=adata.var_names,
            n_jobs=1)

# save results
df = adata.uns["sepal_score"]
df = df.loc[adata.var_names][['sepal_score']]
df = df.reset_index()
df.columns = ['feature_name', 'pred_spatial_var_score']

output = ad.AnnData(var=df,
                    uns={'dataset_id': adata.uns['dataset_id'],
                         'method_id': meta['functionality_name']})

print("Write output to file", flush=True)
output.write_h5ad(par['output'])
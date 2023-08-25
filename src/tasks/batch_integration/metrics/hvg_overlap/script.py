import anndata as ad
from scib.metrics import hvg_overlap

## VIASH START
par = {
    'input_integrated': 'resources_test/batch_integration/pancreas/integrated_embedding.h5ad',
    'output': 'output.h5ad',
}

meta = {
    'functionality_name': 'foo',
}
## VIASH END

print('Read input', flush=True)
adata = ad.read_h5ad(par['input_integrated'])

print('prepare data')
adata_unint = adata.copy()
adata_unint.X = adata_unint.layers["normalized"]
adata.X = adata.layers["corrected_counts"]

print('compute score')

score = hvg_overlap(
    adata_unint,
    adata,
    batch_key="batch"
)

print("Create output AnnData object")
output = ad.AnnData(
    uns={
        "dataset_id": adata.uns['dataset_id'],
        'normalization_id': adata.uns['normalization_id'],
        "method_id": adata.uns['method_id'],
        "metric_ids": [meta['functionality_name']],
        "metric_values": [score]
    }
)

print("Write data to file", flush=True)
output.write_h5ad(par["output"], compression="gzip")
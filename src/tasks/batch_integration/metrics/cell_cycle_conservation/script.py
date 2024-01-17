import anndata as ad
from scib.metrics import cell_cycle
import numpy as np

## VIASH START
par = {
    'input_integrated': 'resources_test/batch_integration/pancreas/integrated_embedding.h5ad',
    'output': 'output.h5ad'
}

meta = {
    'functionality_name': 'foo'
}
## VIASH END

print('Read input', flush=True)
input_solution = ad.read_h5ad(par['input_solution'])
input_integrated = ad.read_h5ad(par['input_integrated'])
input_solution.X = input_solution.layers['normalized']

print('Use gene symbols for features', flush=True)
input_solution.var_names = input_solution.var['feature_name']
input_integrated.var_names = input_integrated.var['feature_name']

translator = {
    "homo_sapiens": "human",
    "mus_musculus": "mouse",
}

print('Compute score', flush=True)
if input_solution.uns['dataset_organism'] not in translator:
    score = np.nan
else:
    organism = translator[input_solution.uns['dataset_organism']]
    score = cell_cycle(
        input_solution,
        input_integrated,
        batch_key='batch',
        embed='X_emb',
        organism=organism,
    )

print('Create output AnnData object', flush=True)
output = ad.AnnData(
    uns={
        'dataset_id': input_solution.uns['dataset_id'],
        'normalization_id': input_solution.uns['normalization_id'],
        'method_id': input_integrated.uns['method_id'],
        'metric_ids': [ meta['functionality_name'] ],
        'metric_values': [ score ]
    }
)


print('Write data to file', flush=True)
output.write_h5ad(par['output'], compression='gzip')

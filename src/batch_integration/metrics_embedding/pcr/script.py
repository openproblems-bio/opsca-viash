## VIASH START
par = {
    'input': './src/batch_integration/embedding/resources/mnn_pancreas.h5ad',
    'output': './src/batch_integration/embedding/resources/cc_score_pancreas_mnn.tsv'
}
## VIASH END

import pprint
import scanpy as sc
from scib.metrics import pcr_comparison

OUTPUT_TYPE = 'embedding'
METRIC = 'pcr'

adata_file = par['input']
output = par['output']

print('Read input', flush=True)
adata = sc.read(adata_file)
adata_int = adata.copy()
name = adata.uns['dataset_id']

print('compute score')
score = pcr_comparison(
    adata,
    adata_int,
    embed='X_emb',
    covariate='batch',
    verbose=False
)

with open(output, 'w') as file:
    header = ['dataset', 'output_type', 'metric', 'value']
    entry = [name, OUTPUT_TYPE, METRIC, score]
    file.write('\t'.join(header) + '\n')
    file.write('\t'.join([str(x) for x in entry]))
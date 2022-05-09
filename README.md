# CovEffect-data-provision
Data provisioning pipeline for GeCo CovEffect's project

![Pipeline plot](pipeline.png)

## Output files for production:
| Path | Destination |
|---|---|
| products/production_metadata/metadata.csv | mariadb/production/metadata |
| products/retrieval/index.tar.gz | extract and move indexdir and its content to backend/api/local_data/ |
| products/similar/embeddings.ann | move to backend/api/local_data/annoy/

## Setup

```sh
# NOTE: if running ploomber <-1.16, remove the --create-env argument
ploomber install --create-env
# activate environment (unix)
source {path-to-venv}/bin/activate
# activate environment (windows cmd.exe)
{path-to-venv}\Scripts\activate.bat
# activate environment (windows PowerShell)
{path-to-venv}\Scripts\Activate.ps0
```


## Running the pipeline

```sh
ploomber build
```



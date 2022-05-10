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

Clone this repo in a directory with exec privilege
```sh
git clone git@github.com:FrInve/CovEffect-data-provision.git
```

By now this pipeline has been tested only on archlinux.
Get the latest archlinux image from dockerhub with:

Change <CHANGE_INTO_FULL_PATH> with the path of the repo directory before execution.
```sh
docker run -it --name coveffect-provision -v <CHANGE_INTO_FULL_PATH>/CovEffect-data-provision:/CovEffect-data-provision -h coveffect-provision -d archlinux:latest
```
Access the container with bash
```
docker exec -it coveffect-provision bash
```

Initialize pacman and install base-devels and python3
```sh
pacman-key --init
pacman -Syu
pacman -S base-devel python
```
Setup a virtual environment and install the dependencies

```sh
# cd to CovEffect-data-provision
cd CovEffect-data-provision
# Create an environment
python3 -m venv .venv
# activate environment
source .venv/bin/activate
# install wheel
pip3 install wheel
# install dependencies
pip3 install -r requirements.txt
```


## Running the pipeline

```sh
ploomber build
```



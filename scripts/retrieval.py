# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
# Whoosh index creation from metadata stage


# %%
# Uncomment the next two lines to enable auto reloading for imported modules
# # %load_ext autoreload
# # %autoreload 2
# For more info, see:
# https://docs.ploomber.io/en/latest/user-guide/faq_index.html#auto-reloading-code-in-jupyter

# %% tags=["parameters"]
# If this task has dependencies, list them them here
# (e.g. upstream = ['some_task']), otherwise leave as None.
upstream = ['clean']

# This is a placeholder, leave it as None
product = None


# %%
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED
from whoosh.analysis import RegexTokenizer, LowercaseFilter, StopFilter
import os, os.path
from whoosh import index, writing
import pandas as pd
from pathlib import Path
import logging
import tarfile
# %%
logger = logging.getLogger(__name__)
# %%
# Import data
data_file_path = upstream['clean']['cleaned_metadata']
df = pd.read_parquet(data_file_path)

# %%
my_analyzer = RegexTokenizer() | LowercaseFilter() | StopFilter()

class CordSchema(SchemaClass):
    cord_uid = ID(stored=True)
    doi = ID
    title = TEXT(analyzer=my_analyzer)
    abstract = TEXT(analyzer=my_analyzer)
    authors = TEXT

# %%
# path/retrieval/index.tar.gz
product_path = Path(str(product['whoosh']))
# make dir path/retrieval
product_path.parent.mkdir(exist_ok=True, parents=True)
# path/retrieval
retrieval_dir = product_path.parent
# make dir path/retrieval/raw_index
(retrieval_dir / 'indexdir').mkdir(exist_ok=True, parents=True)
ix_working_dir = retrieval_dir / 'indexdir'
# %%
if index.exists_in(ix_working_dir):
    ix = index.open_dir(ix_working_dir)
    with ix.writer() as writer:
        writer.mergetype = writing.CLEAR

ix = index.create_in(ix_working_dir, CordSchema)
# %%
with ix.writer() as writer:

    for i in range(len(df)):
        writer.add_document(cord_uid=df.cord_uid.iloc[i],
                            doi=df.doi.iloc[i],
                            title=df.title.iloc[i],
                            abstract=df.abstract.iloc[i],
                            authors=df.authors.iloc[i])
        if i%10000==0:
            #writer.commit()
            print("Indexing paper number " + str(i))
            logger.info("Indexing paper number " + str(i))


# %%
def tardir(path, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(path):
            for file in files:
                tar_handle.add(os.path.join(root, file), arcname='indexir/'+file)

tardir(ix_working_dir, product_path)

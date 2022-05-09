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
# Feature Engineering of CORD-19 SPECTER embeddings
#


# %%
# Uncomment the next two lines to enable auto reloading for imported modules
# # %load_ext autoreload
# # %autoreload 2
# For more info, see:
# https://docs.ploomber.io/en/latest/user-guide/faq_index.html#auto-reloading-code-in-jupyter

# %% tags=["parameters"]
# If this task has dependencies, list them them here
# (e.g. upstream = ['some_task']), otherwise leave as None.
upstream = ['extract_embeddings','clean']

# This is a placeholder, leave it as None
product = None
sample = None

# %%
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from pathlib import Path
from joblib import dump

# %%
df = pd.read_parquet(upstream['clean']['cleaned_metadata'], columns=['cord_uid'])

# %%
if sample:
    dfe = pd.read_csv(upstream['extract_embeddings'], header=None, nrows=200000)
else:
    dfe = pd.read_csv(upstream['extract_embeddings'], header=None)
dfe = dfe.rename({0:"cord_uid"}, axis=1)
print("Shape after loading: " + str(dfe.shape))

# %%
dfe = dfe.drop_duplicates(subset=['cord_uid'], keep='last')
print("Shape after deduplication: " + str(dfe.shape))
# %%
dfe = dfe[dfe.cord_uid.isin(df.cord_uid)]
print("Shape after IsIn clean metadata: " + str(dfe.shape))
# %%
#Normalize the columns
scaler = StandardScaler()
dfe[dfe.columns[1:769]] = scaler.fit_transform(dfe[dfe.columns[1:769]])

# %%
pca_100 = PCA(n_components=100)

dfe_pca_100 = pca_100.fit_transform(dfe.drop(['cord_uid'], axis=1))

# %%
print("Explained variance ration: ")
print(np.sum(pca_100.explained_variance_ratio_))

# %%
# Export PCA model
Path(str(product['pca_100'])).parent.mkdir(exist_ok=True,parents=True)
dump(pca_100, str(product['pca_100']))
# %%
# Export embeddings after PCA
dfe.columns = dfe.columns.astype(str)
dfe.to_parquet(str(product['embeddings_100']))

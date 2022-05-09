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
# Annoy similarity index generation stage for CORD-19
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
upstream = ['embeddings_feature']

# This is a placeholder, leave it as None
product = None


# %%
from annoy import AnnoyIndex
import pandas as pd
from pathlib import Path

# %%
df = pd.read_parquet(upstream['embeddings_feature']['embeddings_100'])

# %%
df['annoy_id'] = range(len(df))
# %%
# Features are the 100 principal components of SPECTER embeddings
features = 100 
t = AnnoyIndex(features,'angular')

# %%
for i in range(len(df)):
    v = df[df.annoy_id== i ].drop(['cord_uid', 'annoy_id'], axis=1).values.tolist()[0]
    t.add_item(i, v)

# %%
t.build(20) # 20 trees
# %%
# Create product directory
Path(str(product['annoy_idx'])).parent.mkdir(exist_ok=True,parents=True)
# %%
t.save(str(product['annoy_idx']))

# %%
df[['cord_uid','annoy_id']].to_parquet(str(product['annoy_metadata']))

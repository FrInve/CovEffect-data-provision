# ---
# jupyter:
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# Prepare metadata for production
# with the index from annoy
# and export to csv


# %%
# Uncomment the next two lines to enable auto reloading for imported modules
# # %load_ext autoreload
# # %autoreload 2
# For more info, see:
# https://docs.ploomber.io/en/latest/user-guide/faq_index.html#auto-reloading-code-in-jupyter

# %% tags=["parameters"]
# If this task has dependencies, list them them here
# (e.g. upstream = ['some_task']), otherwise leave as None.
upstream = ['clean','similar']

# This is a placeholder, leave it as None
product = None


# %%
import pandas as pd
from pathlib import Path

# %%
df = pd.read_parquet(str(upstream['clean']['cleaned_metadata']))
# %%
df_annoy = pd.read_parquet(str(upstream['similar']['annoy_metadata']))

# %%
df.set_index('cord_uid',inplace=True)
df_annoy.set_index('cord_uid',inplace=True)

# %%
df['annoy_id']=df_annoy['annoy_id']
df.reset_index(inplace=True)
# %%
Path(str(product['metadata'])).parent.mkdir(exist_ok=True,parents=True)
df.to_csv(str(product['metadata']))
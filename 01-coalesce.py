# %%

import os
import pandas as pd

# %%

files = [os.path.join("rawdata", f) for f in os.listdir("rawdata")]
df = pd.DataFrame()
for f in files:
    year = int(f.split(".")[0][-4:])
    dff = pd.read_csv(f, names=["name", "gender", "count"])
    dff['year'] = year
    df = pd.concat([df, dff], ignore_index=True)

dff = dff.dropna(axis=0)

df.to_csv("data.csv", index=False)

# %%
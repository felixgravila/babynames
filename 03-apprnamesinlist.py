# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import floor

# %%

df = pd.read_csv("data.csv")
names = df.groupby("name")

nandc = []
for name, namedf in names:
    nandc.append((name, namedf["count"].sum()))

nandc.sort(key=lambda x: x[1], reverse=True)
sortednames = [n[0] for n in nandc]

# %%

pigenavne = set(pd.read_csv("pigenavne.csv")["Navn"].to_list())
drengenavne = set(pd.read_csv("drengenavne.csv")["Navn"].to_list())

allenavne = pigenavne.union(drengenavne)

# %%

scale_factor = 5
aspect_ratio = 4


img = np.zeros(
    (
        round((len(sortednames) / scale_factor) / aspect_ratio),
        round(len(sortednames) / scale_factor),
    )
)

for i, name in enumerate(sortednames):
    if name in allenavne:
        img[:, round(i / scale_factor)] += 1 / scale_factor

plt.figure(figsize=(20, 20 / aspect_ratio))
plt.imshow(img)
plt.yticks([])
xticks = [x * 5000 // scale_factor for x in range(floor(len(sortednames) / 5000) + 1)]
plt.xticks(xticks, [x * scale_factor for x in xticks])
plt.title("Location of DK approved names in ordered list of all US names")
plt.savefig("DKpopularity.png")
plt.show()

# %%

maxprint = 20
for i, (name, count) in enumerate(nandc):
    if maxprint <= 0:
        break
    if name not in allenavne:
        print(f"{name} @ {i} not allowed in DK with {count}")
        maxprint -= 1

# %%

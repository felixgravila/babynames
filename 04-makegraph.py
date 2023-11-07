# %%

import pandas as pd
import matplotlib.pyplot as plt
from math import log10, ceil
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

# %%


pigenavne = set(pd.read_csv("pigenavne.csv")["Navn"].to_list())
drengenavne = set(pd.read_csv("drengenavne.csv")["Navn"].to_list())
allenavne = pigenavne.union(drengenavne)

df = pd.read_csv("data.csv")
df

# %%
# Only names in DK

df = df[df["name"].apply(lambda n: n in allenavne)]
df

# %%
# Only girls

df = df[df["gender"] == "F"]
df

# %%

names = df.groupby("name")

nandc = []
for name, namedf in names:
    nandc.append((name, namedf["count"].sum()))

nandc.sort(key=lambda x: x[1], reverse=True)

# %%
plt.figure(figsize=(10, 5))
plt.plot([log10(n[1]) for n in nandc])

top_log = ceil(log10(nandc[0][1]) + 1)

plt.yticks(range(top_log), [f"{10**x:,}" for x in range(top_log)])

plt.tight_layout()
plt.show()

# %%

"""
Show names around cutoff
"""

CUTOFF_COUNT = 10_000
NUM_NAMES = 50

closest = min(nandc, key=lambda x: abs(x[1] - CUTOFF_COUNT))
place = nandc.index(closest)

print(f"Place is {place}")

for i in range(max(0, place - (50 // 2)), min(len(nandc), place + (50 // 2))):
    if i == place:
        print(">>>> ", end="")
    print(f"{i}\t{nandc[i][0]}: {nandc[i][1]}")


# %%

namesandhgraphs = []
min_year = df["year"].min()
max_year = df["year"].max()

for name, _ in tqdm(nandc[: place + 1]):
    arr = np.zeros((max_year - min_year + 1,))
    a = names.get_group(name)
    for _, (y, c) in a[["year", "count"]].iterrows():
        arr[y - min_year] = c

    arr = arr / arr.max()
    namesandhgraphs.append((name, arr))

# %%

N = len(namesandhgraphs)
graph = np.zeros((N, N))
graph_names = [n for (n, _) in namesandhgraphs]

for i in tqdm(range(0, N - 1)):
    for j in range(i + 1, N):
        graph[i][j] = ((namesandhgraphs[i][1] - namesandhgraphs[j][1]) ** 2).mean()
        graph[j][i] = graph[i][j]

graph = graph / graph.max()
plt.imshow(graph)

# %%

affinities = np.median(graph, axis=0)

print(f"Median graph affinity is {np.median(affinities)}, mean {affinities.mean()}")
print()

sgraph = np.argsort(affinities)
print("Names most affine with others:")
for nidx in sgraph[:10]:
    print(f"{namesandhgraphs[nidx][0]} - {affinities[nidx]}")

print()
print("Names least affine with others:")
for nidx in sgraph[-10:]:
    print(f"{namesandhgraphs[nidx][0]} - {affinities[nidx]}")


# %%


to_find_name = "Elsa"
num_to_plot = 10

to_find_idx = graph_names.index(to_find_name)

plt.figure(figsize=(20, 10), facecolor="white")

plt.plot(
    range(min_year, max_year + 1), namesandhgraphs[to_find_idx][1], label=to_find_name
)

idxs_ranked = np.argsort(graph[to_find_idx])  # first one is itself
for affine_idx in idxs_ranked[1 : num_to_plot + 1]:
    plt.plot(
        range(min_year, max_year + 1),
        namesandhgraphs[affine_idx][1],
        alpha=0.3,
        label=graph_names[affine_idx],
    )

plt.legend()
plt.tight_layout()
plt.show()

# %%
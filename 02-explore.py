# %%

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

orig_df = pd.read_csv(
    "data.csv", dtype={"name": str, "gender": str, "count": int, "year": int}
)
orig_df.head()

df_f = orig_df.groupby("gender").get_group("F")[["name", "count", "year"]]
df_n = df_f.groupby("name")

# %%


def plot_one_name(ax, name, gender, color):
    df_g = orig_df[orig_df["gender"] == gender]
    df_n = df_g.groupby("name").get_group(name)
    ax.plot(df_n["year"], df_n["count"], color=color, label=name)


def plot_names(nandgs):
    fig = plt.figure(figsize=(20, 10), facecolor="white")
    ax = fig.add_subplot(1, 1, 1)
    cmap = plt.get_cmap("jet")
    colors = cmap(np.linspace(0, 1.0, len(nandgs)))
    for (name, gender), color in zip(nandgs, colors):
        plot_one_name(ax, name, gender, color)
    plt.xlabel("Year")
    plt.ylabel("Number of names")
    plt.legend()


# %%


"""
Find names
"""

all_names = list(set(df_f["name"]))
root = "Eve"
names = []
for name in all_names:
    if root in name:
        name_tot_count = df_n.get_group(name)["count"].sum()
        names.append((name, name_tot_count))

names.sort(key=lambda x: x[1], reverse=True)
for name, count in names:
    if count < 1000:
        break
    print(name, count)

# %%

names_to_plot = [("Eveline", "F"), ("Evelyn", "F")]
plt.figure(figsize=(20, 10), facecolor="white")
plot_names(names_to_plot)

# %%

"""
Print most popular names
"""

namepop = []
for gender in ["F"]:
    for n, g in orig_df[orig_df["gender"] == gender].groupby("name"):
        namepop.append((n, g["count"].sum(), gender))

namepop.sort(key=lambda x: x[1], reverse=True)

plot_names([(n[0], n[2]) for n in namepop[:15]])

# %%

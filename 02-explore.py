# %%

import pandas as pd
import matplotlib.pyplot as plt

orig_df = pd.read_csv("data.csv", dtype={"name": str, "gender": str, "count": int, "year": int})
orig_df.head()

df_f = orig_df.groupby("gender").get_group("F")[['name', 'count', 'year']]
df_n = df_f.groupby("name")

# %%

def plot_one_name(ax, name, gender):
    df_g = df[df['gender'] == gender]
    df_n = df_g.groupby("name").get_group(name)
    ax.plot(df_n['year'], df_n['count'], label=name)

def plot_names(names, gender="F"):
    fig = plt.figure(figsize=(20,10), facecolor="white")
    ax = fig.add_subplot(1,1,1)
    for name in names:
        plot_one_name(ax, name, gender)
    plt.legend()

# %%


"""
Find names
"""

all_names = list(set(df_f['name']))
root = "Eve"
names = []
for name in all_names:
    if root in name:
        name_tot_count = df_n.get_group(name)['count'].sum()
        names.append((name, name_tot_count))

names.sort(key=lambda x: x[1], reverse=True)
for name, count in names:
    if count < 1000:
        break
    print(name, count)

# %%

names_to_plot = ["Eveline", "Evelyn"]
plt.figure(figsize=(20,10), facecolor="white")
for name_to_plot in names_to_plot:

"""
Find names with 100 year rule that will be popular in 20 years

rolling average per years and some kind of peak detection
"""
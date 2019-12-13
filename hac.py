import pandas as pd
import math
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


data = pd.read_csv('hac_data.txt')
# print(data)

df = []
groups = []
for i, row in data.iterrows():
    coord = tuple(data.iloc[i].values)
    vals = [coord, i]
    groups.append(vals)

    for j, row in data.iterrows():
        x = data.iloc[i].values
        y = data.iloc[j].values

        distance = round(np.linalg.norm(x-y), 2)

        x = tuple(x)
        y = tuple(y)
        if distance > 0:
            vals = [x, y, distance]
            df.append(vals)


dists = pd.DataFrame(df, columns=['x', 'y', 'distance'])

sorted_dists = dists.sort_values(by=['distance'])
dist_dists = sorted_dists.drop_duplicates('distance').reset_index(drop=True)

# print(dist_dists)
# print(groups)

df_groups = dists = pd.DataFrame(groups, columns=['point', 'group'])
print(dist_dists)
print(df_groups)
color = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080',
         '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']

plt.figure(figsize=(18, 20))
plt.scatter(data['x'], data['y'], color=np.array(
    color)[df_groups['group'].values])
plt.show()

# while df_groups.nunique(0)['group'] > 2:
for l, d_row in dist_dists.iterrows():
    a = dist_dists.iloc[l].values
    x = df_groups.loc[df_groups['point'] == a[0], 'group'].values
    y = df_groups.loc[df_groups['point'] == a[1], 'group'].values
    # print(l)
    # print(
    #     f'a[0] = {a[0]} pos of a[0] = {x[0]} a[1] = {a[1]}  pos of a[1] = {y[0]}')

    if x[0] > y[0]:
        df_groups.loc[df_groups['point'] == a[1], 'group'] = x[0]

        df_groups['group'] = np.where(
            df_groups['group'] == y[0], x[0], df_groups['group'])
    else:
        df_groups.loc[df_groups['point'] == a[1], 'group'] = y[0]
        df_groups['group'] = np.where(
            df_groups['group'] == x[0], y[0], df_groups['group'])

    if df_groups.nunique(0)['group'] < 2:
        break

    print(df_groups)
    plt.figure(figsize=(18, 20))
    plt.scatter(data['x'], data['y'], color=np.array(
        color)[df_groups['group'].values])
    plt.show()

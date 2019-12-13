import pandas as pd
import math
from scipy.spatial.distance import cdist
import numpy as np


data = pd.read_csv('hac_data.txt')
# print(data)

df = []
for i, row in data.iterrows():
    for j, row in data.iterrows():
        x = data.iloc[i].values
        y = data.iloc[j].values

        distance = round(np.linalg.norm(x-y), 2)

        x = tuple(x)
        y = tuple(y)
        if distance > 0:
            vals = [x, y, distance]
            df.append(vals)


dists = pd.DataFrame(df, columns=['x', 'y', 'Distance'])

sorted_dists = dists.sort_values(by=['Distance'])
print(sorted_dists)

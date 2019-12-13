from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering


data = pd.read_csv('hac_data.txt')

# data_scaled = normalize(data)
# data_scaled = pd.DataFrame(data_scaled, columns=data.columns)

cluster = AgglomerativeClustering(
    n_clusters=2, affinity='euclidean', linkage='ward')
# cluster.fit_predict(data_scaled)
cluster.fit_predict(data)
# print(cluster.labels_)


plt.figure(figsize=(18, 20))
# plt.scatter(data_scaled['x'], data_scaled['y'], c=cluster.labels_)
plt.scatter(data['x'], data['y'], c=cluster.labels_)

plt.show()

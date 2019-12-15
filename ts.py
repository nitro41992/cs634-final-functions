import matplotlib.pyplot as plt
from dtw import dtw
import numpy as np

# We define two sequences x, y as numpy array
# where y is actually a sub-sequence from x
y = np.array([0.2, 0.25, 0.3, 0.25, 0.4, 0.45]).reshape(-1, 1)
x = np.array([0.2, 0.3, 0.2, 0.4]).reshape(-1, 1)

dist = []
for i in x:
    for j in y:
        dist.append(round(float(np.square(i-j)), 4))

print(dist)

for x in range(len(dist)):
    left = dist[x-1] if x - 1 <= 0 else float("Inf")
    up = dist[x-6] if x - 6 <= 0 else float("Inf")
    diag = dist[x-7] if x - 7 <= 0 else float("Inf")
    if x == 2:
        print(dist[x], left, x-1, up, diag)
    if x == 0:
        diag = 0
    dist[x] = dist[x] + min(left, up, diag)

print(dist)
# 8 1,2,7
# 9 2,3,8

# def manhattan_distance(x, y): return np.square(x - y)


# d, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=manhattan_distance)
# print(acc_cost_matrix)
# print(path)

# # You can also visualise the accumulated cost and the shortest path

# plt.imshow(acc_cost_matrix.T, origin='lower',
#            cmap='gray', interpolation='nearest')
# plt.plot(path[0], path[1], 'w')
# # plt.show()

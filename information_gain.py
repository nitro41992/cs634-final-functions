import sys
import cmath
import math
import csv
import pandas as pd


data = pd.read_csv('data.txt', header=None)
features = data[0].unique()
# print(features)


for i in features:
    grouped = data.groupby(data.columns[0])
    sub = grouped.get_group(i)

    p_tot = sub.sum()[1]
    n_tot = sub.sum()[2]
    full_tot = p_tot + n_tot
    tot_I = -(p_tot / full_tot)*(cmath.log(p_tot/full_tot, 2)) - \
        (n_tot / full_tot)*(cmath.log(n_tot/full_tot, 2))

    out = []
    for index, row in sub.iterrows():
        p = float(row[1])
        n = float(row[2])
        tot = p + n

        I = -(p / tot)*(cmath.log(p/tot, 2)) - \
            (n / tot)*(cmath.log(n/tot, 2))

        if cmath.isnan(I):
            I = 0

        out_row = [list(row), round(tot/full_tot, 3), round(I.real, 3)]
        out.append(out_row)

    E = []
    for x in range(len(out)):
        E.append(out[x][1] * out[x][2])
        Entropy = round(sum(E), 3)

        Gain = tot_I - Entropy
        vals = [Entropy, round(Gain.real, 3)]

    out.append(vals)
    print(
        f'For Feature {i}, Entropy is {out[-1:][0][0]} and Gain is {out[-1:][0][1]}')

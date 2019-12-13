import sys
import cmath
import csv
import pandas as pd


data = pd.read_csv('data.txt', header=None)
# print(data)
features = data[0].unique()
# print(features)

for i in features:
    grouped = data.groupby(data.columns[0])
    sub = grouped.get_group(i)

    for index, row in sub.iterrows():
        p = float(row[1])
        n = float(row[2])
        row_tot = p + n

        I = -(p / row_tot)*(cmath.log(p/row_tot, 2)) - \
            (n / row_tot)*(cmath.log(n/row_tot, 2))
        print(f'{list(row)},{round(I.real, 3)}')

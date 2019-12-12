import sys
import cmath
import csv


def get_data(filename):
    with open(filename, "rt", encoding='utf8') as f:
        file = csv.reader(f)
        temp = list(file)
    return temp


data = get_data('data.txt')

for i in data:
    p = float(i[1])
    n = float(i[2])
    row_tot = p + n

    I = -(p / row_tot)*(cmath.log(p/row_tot, 2)) - \
        (n / row_tot)*(cmath.log(n/row_tot, 2))
    i.append(round(I.real, 3))

print(data)

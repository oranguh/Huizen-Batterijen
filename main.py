#!/usr/bin/env python

from smart_grid import *
import numpy as np
import csv


# TODO
# DONE read the csv files for houses and batteries.
# DONE determine the range for x and y for each neighborhood.
# populate the grid with houses and batteries with house and battery objects.
# also make wire objects
# create a scoring function which calculates the cost of the smart grid configuration
#
# make algorithms
# ?????
# profit

# we still need to determin the range for each wijk

x_list = []
y_list = []

with open('data/wijk1_huizen.csv') as housereader:
    houses_info = csv.reader(housereader)
    for i, house in enumerate(houses_info):
        if i is 0:
            continue
        x_list.append(int(house[0]))
        y_list.append(int(house[1]))
with open('data/wijk1_batterijen.txt') as f:
    reader = csv.reader(f, csv.excel_tab)
    for i, row in enumerate(reader):
        if i is 0:
            continue
        lala = row[0].strip('[]').split(',')
        x_list.append(int(lala[0]))
        y_list.append(int(lala[1]))

range_x = max(x_list)
range_y = max(y_list)

print(range_x, range_y)
# since 50 is too big I changed them to 5 for now.
range_x = 5
range_y = 5
# Creates numpy matrix where the elements can be anything i.e. objects
grid_matrix = np.zeros((range_x, range_y), dtype="object")

print(grid_matrix)

wijk1 = smart_grid(grid_matrix)

print(wijk1.size)
print(wijk1)

# wijk2 = smart_grid()

# wijk3 = smart_grid()

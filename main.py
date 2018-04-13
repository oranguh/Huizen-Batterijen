#!/usr/bin/env python

from smart_grid import *
import numpy as np
import csv
from termcolor import cprint


# TODO
# DONE read the csv files for houses and batteries.
# DONE maybe make a dictionary containing all battery/houses?
# DONE determine the range for x and y for each neighborhood.
# DONE populate the grid with houses and batteries with house and battery objects.
# also make wire objects?
# create a scoring function which calculates the cost of the smart grid configuration
#
# make algorithms
# ?????
# profit

# we still need to determine the range for each wijk

# lists of all x and y coordinates
x_list = []
y_list = []

# list of dictionary items
houses = []
batteries = []

with open('data/wijk1_huizen.csv') as housereader:
    houses_info = csv.reader(housereader)
    for i, row in enumerate(houses_info):
        # skips header
        if i is 0:
            continue
        # add dictionary item to houses
        houses.append({'x_position': int(row[0]),
         'y_position': int(row[1]), 'output': float(row[2])})

        #  add coordinates to lists
        x_list.append(int(row[0]))
        y_list.append(int(row[1]))

with open('data/wijk1_batterijen.txt') as f:
    reader = csv.reader(f, csv.excel_tab)
    for i, row in enumerate(reader):
        # skips header
        if i is 0:
            continue
        # remove any empty elements
        row = list(filter(None, row))

        # the first element is a bit weird, so had to get it correct
        battery_pos = row[0].strip('[]').split(',')
        # add coordinates to lists
        x_list.append(int(battery_pos[0]))
        y_list.append(int(battery_pos[1]))

        # add dictionary item to batteries
        batteries.append({'x_position': int(battery_pos[0]),
         'y_position': int(battery_pos[1]), 'capacity': float(row[1])})

# find largest values for x and y
range_x = max(x_list) + 1
range_y = max(y_list) + 1

# print(range_x, range_y)
# since 50 is too big I changed them to 5 for now.
# range_x = 5
# range_y = 5

# Creates numpy matrix where the elements can be anything i.e. objects
grid_matrix = np.empty((range_x, range_y), dtype="object")
# print(grid_matrix)
# creates out very own smart_grid object! yay
wijk1 = smart_grid(grid_matrix)

# print(wijk1.size)

# wijk1.create_house([2,3], 500)

# Populate the houses in the smart_grid
for element in houses:
    position = []
    position.append(element['x_position'])
    position.append(element['y_position'])
    wijk1.create_house(position, element['output'])

# populate the batteries in the smart_grid
for element in batteries:
    position = []
    position.append(element['x_position'])
    position.append(element['y_position'])
    wijk1.create_battery(position, element['capacity'])

# pretty display
for row in wijk1.grid:
    for element in row:
        if element is None:
            print('  ', end = "")
        if isinstance(element, smart_battery):
            cprint("B ", 'yellow', end = "")
        if isinstance(element, smart_house):
            print("H ", end = "")
    print('|')

print(batteries)
# print(houses)
print("There are currently {} batteries on the grid".format(wijk1.battery_count))
print("Battery ID: {} has capacity of: {}".format(wijk1.grid[42][3].battery_id, wijk1.grid[42][3].capacity))
print("There are currently {} houses on the grid".format(wijk1.house_count))
print("House ID: {} has output of: {}".format(wijk1.grid[10][27].house_id, wijk1.grid[10][27].output))

print(wijk1.grid[42][3].capacity_left)
wijk1.connect([42, 3], [10, 27])
print(wijk1.grid[42][3].capacity_left)
print(wijk1.calc_cost())

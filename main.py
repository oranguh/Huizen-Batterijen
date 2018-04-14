#!/usr/bin/env python

from smart_grid import *
import numpy as np
import csv
import colorama
from termcolor import cprint


# TODO
# DONE read the csv files for houses and batteries.
# DONE maybe make a dictionary containing all battery/houses?
# DONE determine the range for x and y for each neighborhood.
# DONE populate the grid with houses and batteries with house and battery objects.
# N/A also make wire objects?
# DONE create a scoring function which calculates the cost of the smart grid configuration
#
# Partially DONE make algorithms
# ?????
# profit

colorama.init()

# list of dictionary items
houses = []
batteries = []

# trivial csv reading and writing to dictionary
with open('data/wijk1_huizen.csv') as housereader:
    houses_info = csv.reader(housereader)
    for i, row in enumerate(houses_info):
        # skips header
        if i is 0:
            continue
        # make a position list as [x,y]
        position = []
        position.append(int(row[0]))
        position.append(int(row[1]))
        # add dictionary item to houses
        houses.append({'position': position, 'output': float(row[2])})

with open('data/wijk1_batterijen.txt') as f:
    reader = csv.reader(f, csv.excel_tab)
    for i, row in enumerate(reader):
        # skips header
        if i is 0:
            continue
        # remove any empty elements
        row = list(filter(None, row))
        # the first element is a bit weird, so had to get it correct
        position = row[0].strip('[]').split(',')
        # int cast all elements
        position = [int(x) for x in position]
        # add dictionary item to batteries
        batteries.append({'position': position, 'capacity': float(row[1])})

# find ranges for the grid matrix
max_x = max([dic['position'][0] for dic in houses] +
            [dic['position'][0] for dic in batteries]) + 1
max_y = max([dic['position'][1] for dic in houses] +
            [dic['position'][1] for dic in batteries]) + 1

# print(batteries)
# print(houses)

# creates out very own smart_grid object! yay
wijk1 = SmartGrid(max_x,max_y)

# print(wijk1.size)

# Populate the houses in the smart_grid
for element in houses:
    wijk1.create_house(element['position'], element['output'])

# populate the batteries in the smart_grid
for element in batteries:
    wijk1.create_battery(element['position'], element['capacity'])

# adds dictionaries to the SmartGrid object
wijk1.add_house_dictionaries(houses)
wijk1.add_battery_dictionaries(batteries)


# print("Battery has: {} capacity left".format(wijk1.grid[42][3].capacity_left))
# wijk1.connect([42, 3], [10, 27])

# pretty display
wijk1.prettify()
print("The cost of this grid is: {}".format(wijk1.calc_cost()))

# print("There are currently {} batteries on the grid".format(wijk1.battery_count))
# print("Battery ID: {} has capacity of: {}".format(wijk1.grid[42][3].battery_id, wijk1.grid[42][3].capacity))
# print("There are currently {} houses on the grid".format(wijk1.house_count))
# print("House ID: {} has output of: {}".format(wijk1.grid[10][27].house_id, wijk1.grid[10][27].output))
# print("Battery has: {} capacity left".format(wijk1.grid[42][3].capacity_left))

wijk1.solve()

wijk1.prettify()
print()
print("The cost of this grid is: {}".format(wijk1.calc_cost()))

wijk1.solve('selected_solve')

#!/usr/bin/env python

from smart_grid import *
from read_data import read_data
import numpy as np
import colorama
from termcolor import cprint
import matplotlib.pyplot as plt


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


house_path = 'data/wijk1_huizen.csv'
battery_path = 'data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path)


# find ranges for the grid matrix
max_x = max([dic['position'][0] for dic in houses] +
            [dic['position'][0] for dic in batteries]) + 1
max_y = max([dic['position'][1] for dic in houses] +
            [dic['position'][1] for dic in batteries]) + 1

outputs = [dic['output'] for dic in houses]
print(outputs)

# plt.hist(outputs)
# plt.ylabel('count')
# plt.xlabel('max output')
# plt.show()

# creates our very own smart_grid object! yay
wijk1 = SmartGrid(max_x,max_y)

# Populate the houses in the smart_grid, should I make this a method?
for element in houses:
    wijk1.create_house(element['position'], element['output'])

# populate the batteries in the smart_grid
for element in batteries:
    wijk1.create_battery(element['position'], element['capacity'])

# adds dictionaries to the SmartGrid object
wijk1.add_house_dictionaries(houses)
wijk1.add_battery_dictionaries(batteries)


# print("Battery has: {} capacity left".format(wijk1.grid[42][3].capacity_left))
# wijk1.connect([42, 3 [10, 27])

# pretty display
wijk1.prettify()
print("The cost of this grid is: {}".format(wijk1.calc_cost()))

# print("There are currently {} batteries on the grid".format(wijk1.battery_count))
# print("Battery ID: {} has capacity of: {}".format(wijk1.grid[42][3].battery_id, wijk1.grid[42][3].capacity))
# print("There are currently {} houses on the grid".format(wijk1.house_count))
# print("House ID: {} has output of: {}".format(wijk1.grid[10][27].house_id, wijk1.grid[10][27].output))
# print("Battery has: {} capacity left".format(wijk1.grid[42][3].capacity_left))

# wijk1.solve()

# wijk1.prettify()
# print("The cost of this grid is: {}".format(wijk1.calc_cost()))

wijk1.solve("simple_solve3")

wijk1.prettify()
print("The cost of this grid is: {}".format(wijk1.calc_cost()))

wijk1.cap_left()

house_path = 'data/wijk3_huizen.csv'
houses, batteries = read_data(house_path, battery_path)

x = sorted([house_element['position'] for house_element in houses])
print(x)

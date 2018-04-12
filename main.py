#!/usr/bin/env python

from smart_grid import *
import numpy as np


# TODO
# read the csv files for houses and batteries.
# determine the range for x and y for each neighborhood.
# populate the grid with houses and batteries with house and battery objects.
# also make wire objects
# create a scoring function which calculates the cost of the smart grid configuration
#
# make algorithms
# ?????
# profit

# we still need to determin the range for each wijk
range_x = 10
range_y = 10

# Creates numpy matrix where the elements can be anything i.e. objects
grid_matrix = np.zeros((range_x, range_y), dtype="object")

print(grid_matrix)

wijk1 = smart_grid(grid_matrix)

print(wijk1.size)
print(wijk1)

wijk2 = smart_grid()

wijk3 = smart_grid()

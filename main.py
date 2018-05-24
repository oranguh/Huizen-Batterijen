#!/usr/bin/env python
import sys
import numpy as np
import colorama
from termcolor import cprint
import matplotlib.pyplot as plt

sys.path.append('Code/Helper_Functions')
sys.path.append('Code/Algorithms')
sys.path.append('Data/')
sys.path.append('Results/')

from smart_grid import SmartGrid
from read_data import read_data
from heat_map import heat_map
from solution_reader import solution_reader
from battery_placer import battery_placer


def main():
    colorama.init()


    house_path = 'Data/wijk1_huizen.csv'
    battery_path = 'Data/wijk1_batterijen.txt'

    houses, batteries = read_data(house_path, battery_path)


    # find ranges for the grid matrix
    max_x = max([dic['position'][0] for dic in houses] +
                [dic['position'][0] for dic in batteries]) + 1
    max_y = max([dic['position'][1] for dic in houses] +
                [dic['position'][1] for dic in batteries]) + 1

    # outputs = [dic['output'] for dic in houses]
    # print(outputs)

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
    # for element in batteries:
    #     wijk1.create_battery(element['position'], element['capacity'])

    # adds dictionaries to the SmartGrid object
    wijk1.add_house_dictionaries(houses)
    # wijk1.add_battery_dictionaries(batteries)



    # pretty display
    # wijk1.prettify()
    print("The cost of this grid is: {}".format(wijk1.calc_cost()))

    # solution_reader(wijk1, 'Results/best_brabo_solution.csv')
    # wijk1.solve("simple_solve3")

    # wijk1.prettify()
    print("The cost of this grid is: {}".format(wijk1.calc_cost()))

    # wijk1.cap_left()
    # print("The remaining capacity of batteries are: {}".format(wijk1.bat_cap_left))

    # heat_map(wijk1)

    # wijk1.house_dict_with_manhattan_distances()
    # wijk1.disconnect(houses[1]["position"])

    # house_coordinatesx = [dic['position'][0] for dic in houses]
    # house_coordinatesy = [dic['position'][1] for dic in houses]
    #
    # plt.scatter(house_coordinatesx, house_coordinatesy)
    # plt.show()
    # wijk1.get_lower_bound()
    # print("Lower bound of grid is: {}".format(wijk1.lower_bound))
    battery_placer(wijk1, 10)
    # print(x)
    battery_path = 'Results/Battery_configurations/BESTSCORE_SIGMA_10.csv'
    # battery_path = 'Results/Battery_configurations/1137_nice_sigma10.csv'
    # battery_path = 'Results/Battery_configurations/leuknaampjes.csv'
    houses, batteries = read_data(house_path, battery_path)
    for element in batteries:
        wijk1.create_battery(element['position'], element['capacity'])

    wijk1.add_battery_dictionaries(batteries)
    wijk1.house_dict_with_manhattan_distances()
    heat_map(wijk1)
    wijk1.prettify()
    print(len(wijk1.house_data))

    wijk1.get_lower_bound()
    print("Lower bound of grid is: {}".format(wijk1.lower_bound))
    # DO SIMULATED ANNEALING HERE
    # get the score of the sim annealing, set x to battery placement score. Plot

if __name__ == "__main__":
    main()

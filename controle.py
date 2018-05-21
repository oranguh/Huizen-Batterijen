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
from solution_reader_new_format import solution_reader as solution_reader_new

house_path = 'Data/wijk1_huizen.csv'
# battery_path = 'Data/wijk1_batterijen.txt'
battery_path = 'Results/Battery_configurations/SCORE_4486_SIGMA_10.csv'

houses, batteries = read_data(house_path, battery_path)

max_x = max([dic['position'][0] for dic in houses] +
            [dic['position'][0] for dic in batteries]) + 1
max_y = max([dic['position'][1] for dic in houses] +
            [dic['position'][1] for dic in batteries]) + 1

outputs = [dic['output'] for dic in houses]

wijk1 = SmartGrid(max_x,max_y)

for element in houses:
    wijk1.create_house(element['position'], element['output'])

# populate the batteries in the smart_grid
for element in batteries:
    wijk1.create_battery(element['position'], element['capacity'])

wijk1.add_house_dictionaries(houses)
wijk1.add_battery_dictionaries(batteries)

wijk1.prettify()

# solution_reader_new(wijk1, 'Results/best_hillclimber.json')

wijk1.connect_from_new_structure(wijk1.house_dict_with_manhattan_distances)
heat_map(wijk1)
wijk1.cap_left()
print(wijk1.calc_cost())
print(wijk1.check_validity())

# wijk1.cap_left()
# print(wijk1.calc_cost())
# print(wijk1.check_validity())
#
# print("The remaining capacity of batteries are: {}".format(wijk1.bat_cap_left))

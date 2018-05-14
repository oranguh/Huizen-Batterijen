import sys

sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')
sys.path.append('Code/Helper_Functions')

from smart_grid import SmartGrid
from read_data import read_data
from brabo_solve import node
from brabo_solve2 import solve as solve2

house_path = '../../Data/wijk1_huizen.csv'
battery_path = '../../Data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path, True)

max_x = max([dic['position'][0] for dic in houses] +
            [dic['position'][0] for dic in batteries]) + 1
max_y = max([dic['position'][1] for dic in houses] +
            [dic['position'][1] for dic in batteries]) + 1

wijk1 = SmartGrid(max_x,max_y)
wijk1.add_house_dictionaries(houses)
wijk1.add_battery_dictionaries(batteries)
houses = wijk1.house_dict_with_manhattan_distances



root = node(batteries, houses, 49581)
root.solve()
print("klaar")

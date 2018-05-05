from read_data import read_data
from brabo_solve import *
from brabo_solve2 import solve as solve2

house_path = '../../data/wijk1_huizen.csv'
battery_path = '../../data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path, True)

root = node(batteries, houses, 49581)
root.solve()
print("klaar")

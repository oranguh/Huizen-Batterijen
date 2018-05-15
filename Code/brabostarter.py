from read_data import read_data
from brabo_solve import *
# from brabo_solve2 import solve as solve2

house_path = '../Data/wijk1_huizen.csv'
battery_path = '../Data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path, True)

root = node(batteries, houses, 50000000)
root.solve()
print("klaar")
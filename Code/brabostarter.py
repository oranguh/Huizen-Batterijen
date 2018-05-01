from read_data import read_data
from brabo_solve import *
from brabo_solve2 import solve as solve2

house_path = 'data/wijk1_huizen.csv'
battery_path = 'data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path, True)
# print(type(batteries[0]['capacity']))
# print(type(houses[0]['output']))
root = node(batteries, houses, 77497)
root.solve()
print("klaar")
# solve2(batteries, houses, 77497)
# print("klaar")

import csv
import json
from smart_grid import *
from read_data import read_data
import colorama
from termcolor import cprint

results_path = '../../Results/best_brabo_solution.csv'

house_path = '../../Data/data/wijk1_huizen.csv'
battery_path = '../../Data/data/wijk1_batterijen.txt'

houses, batteries = read_data(house_path, battery_path)


with open(results_path, 'r') as f:
    best_reader = csv.reader(f)
    for i, row in enumerate(best_reader):

        # for some reason the csv contains empty lists?
        if len(row) == 0:
            continue
        if i == 1:
            # print(row[1])
            row[1] = row[1].replace("'", '"')
            parsed_data = json.loads(row[1])
        # print(len(row))


# print(parsed_data['DATA'])
best_houses = parsed_data['DATA']
# print(best_houses[0])

wijk_brabo = SmartGrid(51,51)

wijk_brabo.add_house_dictionaries(houses)
wijk_brabo.add_battery_dictionaries(batteries)

for element in houses:
    wijk_brabo.create_house(element['position'], element['output'])
for element in batteries:
    wijk_brabo.create_battery(element['position'], element['capacity'])
for connectionz in best_houses:
    wijk_brabo.connect(connectionz['connected_to'], connectionz['position'])

wijk_brabo.prettify()
print(wijk_brabo.calc_cost())
wijk_brabo.cap_left()

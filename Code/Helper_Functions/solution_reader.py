import csv
import json
import colorama
from termcolor import cprint
import sys

sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')
from read_data import read_data
from smart_grid import *


def main():
    """ fixed, you can now use this as both a function and as script"""

    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'

    houses, batteries = read_data(house_path, battery_path)

    wijk_brabo = SmartGrid(51,51)
    wijk_brabo.add_house_dictionaries(houses)
    wijk_brabo.add_battery_dictionaries(batteries)

    for element in houses:
        wijk_brabo.create_house(element['position'], element['output'])
    for element in batteries:
        wijk_brabo.create_battery(element['position'], element['capacity'])

    solution_reader(wijk_brabo, '../../Results/best_brabo_solution.csv')

def solution_reader(wijk_brabo, results_path = 'Results/best_brabo_solution.csv'):
    """
    Reads the solution from a file
    """
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

    best_houses = parsed_data['DATA']

    for connectionz in best_houses:
        wijk_brabo.connect(connectionz['connected_to'], connectionz['position'])

    wijk_brabo.prettify()
    print(wijk_brabo.calc_cost())
    wijk_brabo.cap_left()

if __name__ == "__main__":
    main()

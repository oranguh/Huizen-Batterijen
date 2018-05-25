import csv
import json
import colorama
from termcolor import cprint
import sys

sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')
from read_data import read_data
from smart_grid import SmartGrid, SmartHouse, SmartBattery


def main():
    """ fixed, you can now use this as both a function and as script

    """

    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'

    houses, batteries = read_data(house_path, battery_path)

    smart_wijk = SmartGrid(51,51)
    smart_wijk.add_house_dictionaries(houses)
    smart_wijk.add_battery_dictionaries(batteries)

    for element in houses:
        smart_wijk.create_house(element['position'], element['output'])
    for element in batteries:
        smart_wijk.create_battery(element['position'], element['capacity'])

    solution_reader(smart_wijk, '../../Results/best_brabo_solution.csv')

def solution_reader(smart_wijk, results_path = "../../Results/best_brabo_solution.json"):
    """
    Reads the solution from a file
        The new format is a numpy matrix. Each column corresponds to a house.
        Each column is a list of length n + 2. With n being the amount of batteries
        The last element of the list is the output of the house
        the second to last element of the list is the current connection between
        the house and the battery

        The files are stored as json

    """

    with open(results_path) as f:
        parsed_data = json.load(f)

    best_houses = parsed_data['META']['DATA']
    batteries = parsed_data['META']['BATTERIES']

    smart_wijk.house_dict_with_manhattan_distances = best_houses
    smart_wijk.batteries = batteries


if __name__ == "__main__":
    main()

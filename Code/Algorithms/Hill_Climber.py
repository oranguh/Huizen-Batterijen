from itertools import combinations
import sys

sys.path.append('../../Code/Helper_Functions')
sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')

from solution_reader import solution_reader
from read_data import read_data
from smart_grid import *


def main():
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

    hillclimberke = hillclimber(wijk_brabo.house_data, wijk_brabo.battery_dict)

    combs = combinations(range(150), 2)
    ploep = True
    while ploep:
        print("ploep")
        ploep = hillclimberke.run(combs)


class hillclimber:

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries

    def run(self, combs):
        combs = combinations(range(150), 2)
        for i, j in combs:
            if self.swap_check(self.batteries, self.houses[i], self.houses[j]):
                temp = houses[i][-2]
                houses[i][-2] = houses[j][-2]
                houses[j][-2] = temp
                combs = combinations(range(150), 2)
                print("Swap!")
                return
            # print("komt ie dus hier")
        ploep = False
        return ploep


    def swap_check(self, batteries, house1, house2):
        print("Check")
        # if house1[-2] is not house2[-2]:
        print("check2")
        if batteries[house1[-2]].capacity_left < house2[-1] and batteries[house2[-2]].capacity_left < house1[-1]:
            if (house1[house1[-2]] + house2[house2[-2]]) > (house1[house2[-2]] + house2[house1[-2]]):
                return True
        return False


if __name__ == "__main__":
    main()

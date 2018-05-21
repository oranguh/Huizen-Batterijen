from itertools import combinations
from random import shuffle as shuffelke
import sys
import json
import csv

sys.path.append('../../../Code/Helper_Functions')
sys.path.append('../../../Code/Algorithms')
sys.path.append('../../../Data')
sys.path.append('../../../Results')


from solution_reader_new_format import solution_reader
from read_data import read_data
from smart_grid import *


def main():
    house_path = '../../../Data/wijk1_huizen.csv'
    battery_path = '../../../Data/wijk1_batterijen.txt'
    # battery_path = '../../../Results/Battery_configurations/SCORE:4486_SIGMA:10.csv'

    houses, batteries = read_data(house_path, battery_path)

    wijk_brabo = SmartGrid(51,51)
    wijk_brabo.add_house_dictionaries(houses)
    wijk_brabo.add_battery_dictionaries(batteries)

    for element in houses:
        wijk_brabo.create_house(element['position'], element['output'])
    for element in batteries:
        wijk_brabo.create_battery(element['position'], element['capacity'])

    solution_reader(wijk_brabo, "../../../Results/best_brabo_solution.json")
    # print(wijk_brabo.house_dict_with_manhattan_distances)
    hillclimberke = hillclimber(wijk_brabo.house_dict_with_manhattan_distances, wijk_brabo.batteries)
    print(wijk_brabo.batteries)
    combs = []
    comb = combinations(range(150), 2)
    # Creates a list of the combs to be able to call shuffle
    for i in comb:
        combs.append(i)
    ploep = True
    while ploep:
        ploep = hillclimberke.run(combs)

    with open("../../../Results/best_hillclimber.json", 'w') as jsonfile:
        json.dump({"META": {"DATA": hillclimberke.houses, "BATTERIES": hillclimberke.batteries}}, jsonfile)
    with open("../../../Results/best_hillclimber.csv1", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["score", "configuration"])
        writer.writerow([hillclimberke.calc_cost(), {"DATA": hillclimberke.houses}])

    hillclimberke.calc_cost()


class hillclimber:

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries
        self.swaps = 0

    def run(self, combs):
        shuffelke(combs)
        for i, j in combs:
            # Nog batterij capaciteit aanpassen
            if self.swap_check(self.houses[i], self.houses[j]):
                battery_index = self.houses[i][-2]
                battery_jndex = self.houses[j][-2]
                self.batteries[battery_index]['capacity'] += (self.houses[i][-1] - self.houses[j][-1])
                self.batteries[battery_jndex]['capacity'] += (self.houses[j][-1] - self.houses[i][-1])
                temp = self.houses[i][-2]
                self.houses[i][-2] = self.houses[j][-2]
                self.houses[j][-2] = temp
                self.swaps += 1
                return True
        print("beste gevonden")
        print("swaps: ")
        print(self.swaps)
        return False


    def swap_check(self, house1, house2):
        if house1[-2] is not house2[-2]:
            if (self.batteries[house1[-2]]['capacity'] + house1[-1]) >= house2[-1] and (self.batteries[house2[-2]]['capacity'] + house2[-1]) >= house1[-1]:
                if (house1[house1[-2]] + house2[house2[-2]]) > (house1[house2[-2]] + house2[house1[-2]]):
                    return True
        return False

    def calc_cost(self):
        total_cost = 0
        for house in self.houses:
            total_cost += house[house[-2]]

        return total_cost


if __name__ == "__main__":
    main()

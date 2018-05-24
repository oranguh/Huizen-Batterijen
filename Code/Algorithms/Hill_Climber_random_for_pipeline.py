from itertools import combinations
from random import shuffle as shuffelke
import sys
import json
import csv

sys.path.append('../../Code/Helper_Functions')
sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')


from solution_reader_new_format import solution_reader
from read_data import read_data
from smart_grid import *


def main():

    # Paths to the houses and batteries compositions
    house_path = '../../Data/wijk1_huizen.csv'
    # battery_path = '../../Data/wijk1_batterijen.txt'
    # battery_path = '../../Results/Battery_configurations/SCORE:4486_SIGMA:10.csv'
    battery_path = '../../Results/Battery_configurations/1137_nice_sigma10.csv'

    # Gets the houses and batteries
    houses, batteries = read_data(house_path, battery_path)

    # Creates and fills the smartgrid so that we can use the functionality
    wijk = SmartGrid(51,51)
    wijk.add_house_dictionaries(houses)
    wijk.add_battery_dictionaries(batteries)

    for element in houses:
        wijk.create_house(element['position'], element['output'])
    for element in batteries:
        wijk.create_battery(element['position'], element['capacity'])


    count = 0
    best_score = 1000000000

    # runs the Hillclimber a 100 times
    while count < 100:
        count += 1

        # Gets the start position from a certain result
        solution_reader(wijk_brabo, "../../Results/best_brabo_solution_1337.json")

        # Initializes the hillclimber
        hillclimberke = hillclimber(wijk.house_dict_with_manhattan_distances, wijk_brabo.batteries)

        # Creates a list of the combs to be able to call shuffle
        combs = []
        comb = combinations(range(150), 2)
        for i in comb:
            combs.append(i)

        # Keeps hillclimbing untill no better option is found (ploep = false)
        ploep = True
        while ploep:
            ploep = hillclimberke.run(combs)

        # If no hillclimber is in optimum, check if best score, if so print it.
        if hillclimberke.calc_cost() < best_score:
            with open("../../Results/best_hc_1337.json", 'w') as jsonfile:
                json.dump({"META": {"DATA": hillclimberke.houses, "BATTERIES": hillclimberke.batteries}}, jsonfile)
            with open("../../Results/best_hc_1337.csv1", "w") as f:
                writer = csv.writer(f)
                writer.writerow(["score", "configuration"])
                writer.writerow([hillclimberke.calc_cost(), {"DATA": hillclimberke.houses}])

    print(best_score)


# Class in which a hillclimber is initialized with some functions to run, check and calculate costs
class hillclimber:

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries
        self.swaps = 0

    # run starts the hillclimbing proces
    def run(self, combs):
        # Shuffles the list of combinations then loops through all the possible combinations
        shuffelke(combs)
        for i, j in combs:
            if self.swap_check(self.houses[i], self.houses[j]):

                # Updates the batteries
                self.batteries[self.houses[i][-2]]['capacity'] += (self.houses[i][-1] - self.houses[j][-1])
                self.batteries[self.houses[j][-2]]['capacity'] += (self.houses[j][-1] - self.houses[i][-1])

                # Updates the houses and increments the swaps
                temp = self.houses[i][-2]
                self.houses[i][-2] = self.houses[j][-2]
                self.houses[j][-2] = temp
                self.swaps += 1
                return True

        print("best found, number of swaps: ")
        print(self.swaps)

        # Returns false only if all combinations have been checked and no steps could be made
        return False


    # swap_check checks if the propose swap is legal
    def swap_check(self, house1, house2):

        # First checks if houses are on different batteries
        if house1[-2] is not house2[-2]:

            # Then checks if the swap is legal regarding capacity
            if (self.batteries[house1[-2]]['capacity'] + house1[-1]) >= house2[-1] and (self.batteries[house2[-2]]['capacity'] + house2[-1]) >= house1[-1]:

                # Then checks whether the swap would be an impovement
                if (house1[house1[-2]] + house2[house2[-2]]) > (house1[house2[-2]] + house2[house1[-2]]):
                    return True
            return False

    # calc_cost loops through the houses to calculate the total cost of the solution
    def calc_cost(self):
        total_cost = 0
        for house in self.houses:
            total_cost += house[house[-2]]
        return total_cost


if __name__ == "__main__":
    main()

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
from smart_grid import SmartGrid, SmartHouse, SmartBattery

# Class in which a hillclimber is initialized with some functions to run, check and calculate costs
class Hillclimber:
    """
    Hillclimber object takes as input batteries dictionary and houses dictionary (new format)

    has method calc_cost(self) which returns the cost of the configurations

    If you want to have the best configuration you can use the property Hillclimber.houses

    """

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries
        self.swaps = 0
        self.combs = []
        comb = combinations(range(150), 2)
        for i in comb:
            self.combs.append(i)


    # run starts the hillclimbing proces
    def run(self):
        # Shuffles the list of combinations then loops through all the possible combinations
        # print("GOAN we")
        shuffelke(self.combs)
        for i, j in self.combs:
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

        print("hillclimber finished, number of swaps: {}".format(self.swaps))

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

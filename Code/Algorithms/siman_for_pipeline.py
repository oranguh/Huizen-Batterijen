from itertools import combinations
import random
import math
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

# Class in which you can initialze a simulated annealing, run it and some extra functionality
class Simulated_annealing:
    """
        Simulated annealing

        By using a solved grid simulated annealing tries to randomly make swaps.
        Depending on the cooling scheme used different results will follow.

        heatscheme:
            linear
            exponential
            sigmoid

        The Simulated_annealing object takes as input a battery dictionary and
        a houses dictionary (new format)
        The Simulated_annealing object has the method calc_cost()
        which returns the cost
    """
    def __init__(self, houses, batteries, combs):
        self.houses = houses
        self.batteries = batteries
        self.accepted = 0
        self.iterations = 0
        self.combs = combs
        # 1 miljoen geeft ongeveer beste scores, niet handig voor testen
        self.maxiterations = 1000

    # Starts the simulated annealing procces
    def run(self):
        while self.iterations < self.maxiterations:
            self.iterations += 1
            comb = random.choice(self.combs)
            i = comb[0]
            j = comb[1]

            if self.swap_check(self.houses[i], self.houses[j]):

                # If swap was accepted, update battery capacity and the houses
                self.batteries[self.houses[i][-2]]['capacity'] += (self.houses[i][-1] - self.houses[j][-1])
                self.batteries[self.houses[j][-2]]['capacity'] += (self.houses[j][-1] - self.houses[i][-1])
                temp = self.houses[i][-2]
                self.houses[i][-2] = self.houses[j][-2]
                self.houses[j][-2] = temp
                return True
        print("gecalculeerde kosten: {}".format(self.calc_cost()))
        return False


    def swap_check(self, house1, house2, heatscheme = "sigmoid"):
        if house1[-2] is not house2[-2]:
            if (self.batteries[house1[-2]]['capacity'] + house1[-1]) >= house2[-1] and (self.batteries[house2[-2]]['capacity'] + house2[-1]) >= house1[-1]:
                gain = (house1[house1[-2]] + house2[house2[-2]]) - (house1[house2[-2]] + house2[house1[-2]])

                if heatscheme == "linear":
                    temperature = 10000 * (20/10000) ** (self.iterations / self.maxiterations)
                elif heatscheme == "exponential":
                    temperature = 80000 - self.iterations * (80000/20) /self.maxiterations
                else:
                    sigfactor = self.maxiterations/(3000)
                    temperature = 20 + ((8000 -20) / (1 + math.exp(0.3 * ((self.iterations - self.maxiterations/2)/sigfactor))))

                chance = math.e ** (gain/temperature)
                if chance > random.random():
                    self.accepted += 1
                    return True
        return False

    def calc_cost(self):
        total_cost = 0
        for house in self.houses:
            total_cost += house[house[-2]]
        # print("simulated annealing cost: {}".format(total_cost))
        return total_cost

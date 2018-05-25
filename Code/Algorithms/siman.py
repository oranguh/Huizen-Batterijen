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


def main():
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

    heatscheme = "exponential"

    # Sets paths to house and battery compositions
    house_path = '../../Data/wijk1_huizen.csv'
    # battery_path = '../../Data/wijk1_batterijen.txt'
    # battery_path = '../../Results/Battery_configurations/SCORE:4486_SIGMA:10.csv'
    battery_path = '../../Results/Battery_configurations/lucas_1137_nice_sigma10.csv'

    # Reads the data and puts it in a smartgrid for functinonality
    houses, batteries = read_data(house_path, battery_path)
    wijk_brabo = SmartGrid(51,51)
    wijk_brabo.add_house_dictionaries(houses)
    wijk_brabo.add_battery_dictionaries(batteries)

    for element in houses:
        wijk_brabo.create_house(element['position'], element['output'])
    for element in batteries:
        wijk_brabo.create_battery(element['position'], element['capacity'])

    count = 0
    best_score = 1000000000

    # Runs the simulated annealing 100 times
    while count < 100:
        count += 1

        # Gets the startposition from a certain result and intializes the simulated annealing
        # solution_reader(wijk_brabo, "../../Results/best_brabo_solution_marco.json")
        solution_reader(wijk_brabo, "../../Results/best_brabo_solution_1337.json")
        siman = Simulated_annealing(wijk_brabo.house_dict_with_manhattan_distances, wijk_brabo.batteries)

        # makes a list of all possible legal and illegal swaps
        combs = []
        comb = combinations(range(150), 2)
        for i in comb:
            combs.append(i)

        # Runs the simulated annealing untill max iterations are reached
        while siman.iterations < siman.maxiterations:
            siman.run(random.choice(combs))

        # If better score is found, save it
        if best_score > siman.calc_cost():
            best_score = siman.calc_cost()
        #     with open("../../Results/best_siman_hc_1.json", 'w') as jsonfile:
        #         json.dump({"META": {"DATA": siman.houses, "BATTERIES": siman.batteries}}, jsonfile)
        #     with open("../../Results/best_siman_hc_1.csv1", "w") as f:
        #         writer = csv.writer(f)
        #         writer.writerow(["score", "configuration"])
        #         writer.writerow([siman.calc_cost(), {"DATA": siman.houses}])

    print(best_score)


# Class in which you can initialze a simulated annealing, run it and some extra functionality
class Simulated_annealing:

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries
        self.accepted = 0
        self.iterations = 0
        # 1 miljoen geeft ongeveer beste scores, niet handig voor testen
        self.maxiterations = 1000000

    # Starts the simulated annealing procces
    def run(self, combs):
        while self.iterations < self.maxiterations:
            self.iterations += 1
            i = combs[0]
            j = combs[1]

            if self.swap_check(self.houses[i], self.houses[j]):

                # If swap was accepted, update battery capacity and the houses
                self.batteries[self.houses[i][-2]]['capacity'] += (self.houses[i][-1] - self.houses[j][-1])
                self.batteries[self.houses[j][-2]]['capacity'] += (self.houses[j][-1] - self.houses[i][-1])
                temp = self.houses[i][-2]
                self.houses[i][-2] = self.houses[j][-2]
                self.houses[j][-2] = temp
                return True
        return False


    def swap_check(self, house1, house2):
        if house1[-2] is not house2[-2]:
            if (self.batteries[house1[-2]]['capacity'] + house1[-1]) >= house2[-1] and (self.batteries[house2[-2]]['capacity'] + house2[-1]) >= house1[-1]:
                gain = (house1[house1[-2]] + house2[house2[-2]]) - (house1[house2[-2]] + house2[house1[-2]])

                # Various heating schemes
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

        return total_cost



if __name__ == "__main__":
    main()

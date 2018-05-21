from itertools import combinations
from random import shuffle as shuffelke
import sys

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
    combs = combinations(range(150), 2)
    ploep = True
    while ploep:
        ploep = hillclimberke.run(combs)



class hillclimber:

    def __init__(self, houses, batteries):
        self.houses = houses
        self.batteries = batteries

    def run(self, combs):
        besti, bestj
        for i, j in combs:
            # Nog batterij capaciteit aanpassen
            if self.swap_check(self.batteries, self.houses[i], self.houses[j]):
                battery_index = self.houses[i][-2]
                battery_jndex = self.houses[j][-2]
                self.batteries[battery_index]['capacity'] += self.houses[i][-1]
                self.batteries[battery_index]['capacity'] -= self.houses[j][-1]
                self.batteries[battery_jndex]['capacity'] += (self.houses[j][-1] - self.houses[i][-1])
                temp = self.houses[i][-2]
                self.houses[i][-2] = self.houses[j][-2]
                self.houses[j][-2] = temp
                print("Swap!")
                return True
        print("beste gevonden")
        return False


    def swap_check(self, i, j):
        if self.houses[i][-2] is not self.houses[j][-2]:
            if (self.batteries[self.houses[i][-2]]['capacity'] + self.houses[i][-1]) >= self.houses[j][-1] and (self.batteries[self.houses[j][-2]]['capacity'] + self.houses[j][-1]) >= self.houses[i][-1]:
                if (self.houses[i][self.houses[i][-2]] + self.houses[j][self.houses[j][-2]]) > (self.houses[i][self.houses[j][-2]] + self.houses[j][self.houses[i][-2]]):
                    return i , j
        return False

    def best_swap(self, combs):
        besti, bestj = 0, 0
        for i, j  in combs:
            i , j = self.swap_check(i, j)






if __name__ == "__main__":
    main()

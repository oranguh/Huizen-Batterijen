# from ..Helper_Functions.smart_grid import *
import random
import csv
import matplotlib.pyplot as plt
import sys

sys.path.append('../../Code/Algorithms')
sys.path.append('../../Code/Helper_Functions')
sys.path.append('../../Results')
from read_data import read_data
from smart_grid import *

def main():

    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'

    houses, batteries = read_data(house_path, battery_path)

    wijk1 = SmartGrid(51,51)
    wijk1.add_house_dictionaries(houses)
    wijk1.add_battery_dictionaries(batteries)

    for element in houses:
        wijk1.create_house(element['position'], element['output'])
    for element in batteries:
        wijk1.create_battery(element['position'], element['capacity'])

    random_solve(wijk1)
    print("klaar")


def random_solve(the_grid):
    """    """

    print("\n\n\n")
    print("You are now using random_solve!")
    # cap_limit telling the iterator to stop when battery_cap below this value

    # get number of batteries
    n_bat = len(the_grid.battery_dict)
    # count to keep looping through batteries, keep count to keep track of number of failures
    bat_pos = [dic['position'] for dic in the_grid.battery_dict]
    solutions_list = []
    # best_score = 80000
    limit = 4000

    for i in range(limit):
        # Iterates through nearest houses until cap full
        keepcount = 0
        count = 0
        for house_pos in shuffle(the_grid):

            if keepcount is n_bat:
                break
            while not the_grid.connect(bat_pos[count], house_pos):
                #print("Failed to connect")
                count += 1
                keepcount += 1

                if count is n_bat:
                    count = 0
                if keepcount is n_bat:
                    break
            else:
                #print("connected battery: {} with house {}".format(bat_pos, house_pos))
                continue

        score = the_grid.calc_cost()
        solutions_list.append(score)

        house_path = '../../Data/wijk1_huizen.csv'
        battery_path = '../../Data/wijk1_batterijen.txt'

        houses, batteries = read_data(house_path, battery_path)

        the_grid = SmartGrid(51,51)
        the_grid.add_house_dictionaries(houses)
        the_grid.add_battery_dictionaries(batteries)

        for element in houses:
            the_grid.create_house(element['position'], element['output'])
        for element in batteries:
            the_grid.create_battery(element['position'], element['capacity'])
        # if score < best_score:
        #     best_score = score
        #     best_list = house_pos
    with open("../../Results/random_solutions.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(solutions_list)

    # print(solutions_list)
    title_string = 'Random solve distribution n = ' + str(limit)
    plt.hist(solutions_list, 50, facecolor='blue')
    plt.xlabel('Grid Score')
    plt.ylabel('Count')
    plt.title(title_string)
    plt.show()
    # return the_grid.grid



def shuffle(the_grid):
    """ returns sorted list of all houses_positions snearest to battery using manhattan distance
        takes whole SmartGrid object as argument
    """

    # creates list of all coordinates
    positions_house = [dic['position'] for dic in the_grid.house_dict]
    random.shuffle(positions_house)

    return positions_house


if __name__ == "__main__":
    main()

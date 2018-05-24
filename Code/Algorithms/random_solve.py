# from ..Helper_Functions.smart_grid import *
import random
import numpy as np

def random_solve(the_grid, a_limit = 10):
    """    """

    print("\n\n\n")
    print("You are now using random_solve!")
    # cap_limit telling the iterator to stop when battery_cap below this value
    houses = the_grid.house_dict
    batteries = the_grid.battery_dict
    # get number of batteries
    n_bat = len(the_grid.battery_dict)
    # count to keep looping through batteries, keep count to keep track of number of failures
    bat_pos = [dic['position'] for dic in the_grid.battery_dict]
    best_list = []
    best_score = 80000
    # the_grid.grid = np.empty((51, 51), dtype="object")
    limit = a_limit
    i = 0
    while i < limit:
        # Reset grid
        the_grid.grid = np.empty((51, 51), dtype="object")
        for element in houses:
            the_grid.create_house(element['position'], element['output'])
        for element in batteries:
            the_grid.create_battery(element['position'], element['capacity'])
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
                # print("hey")

                if count is n_bat:
                    count = 0
                if keepcount is n_bat:
                    break
            else:
                #print("connected battery: {} with house {}".format(bat_pos, house_pos))
                continue
        if the_grid.check_validity():
            i += 1
            score = the_grid.calc_cost()
            if score < best_score:
                best_score = score
                best_list = house_pos

    # print(best_score)
    return the_grid.grid



def shuffle(the_grid):
    """ returns sorted list of all houses_positions snearest to battery using manhattan distance
        takes whole SmartGrid object as argument
    """

    # creates list of all coordinates
    positions_house = [dic['position'] for dic in the_grid.house_dict]
    random.shuffle(positions_house)

    return positions_house

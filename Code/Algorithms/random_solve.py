# from ..Helper_Functions.smart_grid import *
import random
import numpy as np
import copy
def random_solve(the_grid, limit = 10):
    """
        randomly tries to generate a VALID solution to the grid
        This can take a very long time depending on the amount of batteries there are

        Typically for 5 batteries, one in every 100 random solutions will be
        valid. However, when you have more batteries, the chance to get
        a random valid solution decreases greatly

        If random_solve takes too long to find a solution, false is returned

        Otherwise the best solution


    """

    print("\n\n")
    print("You are now using random_solve!")
    # cap_limit telling the iterator to stop when battery_cap below this value
    houses = the_grid.house_dict
    batteries = the_grid.battery_dict
    # get number of batteries
    n_bat = len(the_grid.battery_dict)
    # count to keep looping through batteries, keep count to keep track of number of failures
    bat_pos = [dic['position'] for dic in the_grid.battery_dict]
    best_list = []
    best_score = 999999999
    # the_grid.grid = np.empty((51, 51), dtype="object")
    i = 0
    infinite_loop_counter = 0
    while i < limit:
        # Reset grid
        the_grid.grid = np.empty((51, 51), dtype="object")
        the_grid.house_count = 0
        the_grid.battery_count = 0
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
                infinite_loop_counter += 1
                if infinite_loop_counter > 1000000:
                    print("maximum reached inner")
                    if i == 0:
                        return False
                    else:
                        return best_grid
                if count is n_bat:
                    count = 0
                if keepcount is n_bat:
                    break
            else:
                #print("connected battery: {} with house {}".format(bat_pos, house_pos))
                continue
        if the_grid.check_validity():
            i += 1
            infinite_loop_counter = 0
            score = the_grid.calc_cost()
            if score < best_score:
                best_score = score
                best_list = house_pos
                best_grid = copy.deepcopy(the_grid.grid)
        else:
            infinite_loop_counter += 1
            if infinite_loop_counter > 100000:
                print("maximum reached outer")
                if i == 0:
                    return False
                else:
                    return best_grid

    # print(best_score)
    return best_grid



def shuffle(the_grid):
    """ returns sorted list of all houses_positions snearest to battery using manhattan distance
        takes whole SmartGrid object as argument
    """

    # creates list of all coordinates
    positions_house = [dic['position'] for dic in the_grid.house_dict]
    random.shuffle(positions_house)

    return positions_house

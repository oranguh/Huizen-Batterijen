# from ..Helper_Functions.smart_grid import *

def simple_solve3(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid

        General idea:
        makes a list with the houses sorted on descending order on output. Then tries
        to fill a battery untill the output is more then the capacity_left, then fills the next
        battery untill all houses are connected!

        BONUS:
        maybe looping through houses instead might be better?
    """

    print("\n\n\n")
    print("You are now using simple_solve2!")

    # gets number of batteries
    n_bat = len(the_grid.battery_dict)

    # count to keep looping through batteries
    count = 0
    bat_pos = [dic['position'] for dic in the_grid.battery_dict]
    print(bat_pos[0])

    # Iterates through houses until it doesn't fit in the current battery, then tries next
    for house_pos in sort_on_output(the_grid):
        # print(count)
        while not the_grid.connect(bat_pos[count], house_pos):
            print("Failed to connect")
            count += 1
            if count == n_bat:
                count = 0
                continue
        else:
            print("connected battery: {} with house {}".format(bat_pos, house_pos))
            continue


    return the_grid.grid

def sort_on_output(the_grid):
    """ returns sorted list of all houses_positions based on output
        with largest output first
    """

    # creates list of all coordinates
    positions_house = [dic['position'] for dic in the_grid.house_dict]

    # creates list of outputs per house
    outputs = []
    for pos in positions_house:
        outputs.append(the_grid.grid[pos[0]][pos[1]].output)

    # here I have 2 lists of equal size. I sort both, basing the sort on the output
    outputs, positions_house = zip(*sorted(zip(outputs, positions_house), reverse=True))


    return positions_house

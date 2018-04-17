from smart_grid import *

def simple_solve2(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid

        General idea:
        Loops through every battery and keeps connecting to the closest house until
        the capacity is reached.

        BONUS:
        maybe looping through houses instead might be better?
    """

    print("\n\n\n")
    print("You are now using simple_solve!")
    # cap_limit telling the iterator to stop when battery_cap below this value
    cap_limit = 20

    # loop though every battery
    for house in the_grid.house_dict:
        house_pos = house['position']
        print(house_pos)
        output = the_grid.grid[house_pos[0]][house_pos[1]].output
        print(output)

        sort_on_output(the_grid)
        # print("Now connecting battery: {}".format(bat_pos))
        # Iterates through nearest houses until cap full
        for house_pos in find_nearest_unconnected_houses(bat_pos, the_grid):
            # print("capacity left: {}".format(the_grid.grid[bat_pos[0]][bat_pos[1]].capacity_left))

            # keep connecting to battery until the cap is close to full
            if the_grid.grid[bat_pos[0]][bat_pos[1]].capacity_left < cap_limit:
                # print("Capacity reached")
                break
            if not the_grid.grid[house_pos[0]][house_pos[1]].battery_connect is None:
                continue
            if the_grid.connect(bat_pos, house_pos):
                # print("connected battery: {} with house {}".format(bat_pos, house_pos))
                continue
            else:
                # print("Failed to connect")
                continue

    return the_grid.grid

def sort_on_output(the_grid):
    """ returns sorted list of all houses_positions snearest to battery using manhattan distance
        takes whole SmartGrid object as argument
    """

    # creates list of all coordinates
    positions_house = [dic['position'] for dic in the_grid.house_dict]
    print(positions_house)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # creates list of manhattan distance per coordinate in relation to the battery distance
    outputs = []
    for pos in positions_house:
        outputs.append(the_grid.grid[pos[0]][pos[1]].output)
    print(outputs)
    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    # here I have 2 lists of equal size. I sort both, basing the sort on the manhattan distance
    outputs1 = sorted(zip(outputs, positions_house), reverse=True)
    print(outputs1)

    # print(positions_house)
    # print(manhattan_distances)

    return positions_house

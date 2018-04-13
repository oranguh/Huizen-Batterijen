from smart_grid import *

def simple_solve(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid"""

    print("\n\n\n")
    print("You are now using simple_solve!")

    # loop though every battery
    for battery in the_grid.battery_dict:
        bat_pos = [battery['x_position'], battery['y_position']]

        print("Now connecting battery: {}".format(bat_pos))
        # Iterates through nearest houses until cap full
        for house_pos in find_nearest_unconnected_houses(bat_pos, the_grid):
            print("capacity left: {}".format(the_grid.grid[bat_pos[0]][bat_pos[1]].capacity_left))

            # keep connecting to battery until the cap is close to full
            if the_grid.grid[bat_pos[0]][bat_pos[1]].capacity_left < 20:
                print("Capacity reached")
                break
            if the_grid.connect(bat_pos, house_pos):
                print("connected battery: {} with house {}".format(bat_pos, house_pos))
            else:
                print("Failed to connect")

    return the_grid.grid

def find_nearest_unconnected_houses(battery_position, the_grid):
    """ returns ordered list of all houses nearest to battery using manhattan distance"""

    positions_house = [[dic['x_position'], dic['y_position']] for dic in the_grid.house_dict]
    manhattan_distances = []
    for pos in positions_house:
        manhattan_distances.append((abs(pos[0] - battery_position[0]) + abs(pos[1] - battery_position[1])))

    manhattan_distances, positions_house = zip(*sorted(zip(manhattan_distances, positions_house)))

    # print(positions_house)
    # print(manhattan_distances)

    return positions_house

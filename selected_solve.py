from smart_grid import *

def selected_solve(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid

        General idea:
        Weighted solve works by calculating the manhattan distances per house per battery.

        i.e. {'distance_to_[x, y]': 5, 'distance_to_[x, y]': 18, 'distance_to_[x, y]': 40}
        with [x, y] being the coordinates of various batteries

        Pseudocode:
        Finds houses which are only close to 1 battery.
            Of those it selects houses with lowest output and connects them first.
            Then it connects houses of higher output
        Finds houses which are only close to 2 batteries.
            Of those it selects houses with lowest output and connects them first.
            Then it connects houses of higher output
        Finds houses which are only close to .... etc. etc.


        BONUS:
        Once a battery is filled to capacity, do I need to make sure that the battery
        is not longer being considered for further calculations?
    """
    print("\n\n\n")
    print("You are now using selected_solve!")

    the_grid.house_dict = house_dict_with_manhattan_distances(the_grid)

    print(the_grid.house_dict[0:3])

    return the_grid.grid

def house_dict_with_manhattan_distances(the_grid):
    """
        updates the house_dict to contain the manhattan distances to each battery

        the keys names are as follows: ['distance_to_[x,y]']
        where x,y are the coordinates of the battery

        takes as input a SmartGrid and returns the updated SmartGrid.house_dict
    """

    for battery in the_grid.battery_dict:
        battery_pos = battery['position']
        for i,house in enumerate(the_grid.house_dict):
            key_string = 'distance_to_' + str(battery_pos)
            house_pos = house['position']
            the_grid.house_dict[i][key_string] = [
            battery_pos,
            abs(house_pos[0] - battery_pos[0]) +
            abs(house_pos[1] - battery_pos[1])]

    return the_grid.house_dict

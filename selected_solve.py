from smart_grid import *
import numpy as np
import matplotlib.pyplot as plt

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


    all_batteries = [dic_item['position'] for dic_item in the_grid.battery_dict]
    all_batteries = ['distance_to_' + str(dic_item) for dic_item in all_batteries]
    all_distances = []

    # nested list comprehension? not sure if it's alright to do that so instead just a normal for loop
    for i in range(len(all_batteries)):
        all_distances += [dic_item[all_batteries[i]][1] for dic_item in the_grid.house_dict]
    # print(all_distances)
    q75, q50, q25 = np.percentile(all_distances, [75, 50 ,25])

    print("The iqr 75, 50, 25 are: {}, {}, {} \n".format(q75, q50, q25))
    for house in the_grid.house_dict:
        connections = [house[battery] for battery in all_batteries]
        under_q25 = [(q25 <= connect[1]) for connect in connections]
        above_q75 = [(q75 >= connect[1]) for connect in connections]

        # print(sum(under_q25))
        if (sum(under_q25) == 1) and (sum(above_q75) == 4):
            print("close to only 1")
            # print(under_q25)
            # print(above_q75)
            best_connections = []
            for i in range(len(all_batteries)):
                  best_connections += [house[all_batteries[i]]]
            # must use numpy to index array in an easy way
            best_connections = np.array(best_connections)
            # print(best_connections[:,0])
            best = best_connections[np.argmin(best_connections[:,1]),0]
            if the_grid.connect(best, house['position']):
                print("connected battery: {} with house {}".format(best, house['position']))
            else:
                print("Failed to connect")

        # if (sum(under_q25) == 2) and (sum(above_q75) == 3):
        #     print("2, 3")
        #     print(under_q25)
        #     print(above_q75)
        # if sum(under_q25) == 3 and sum(above_q75) == 2:
        #     print("3, 2")
        #     print(under_q25)
        #     print(above_q75)
        # if sum(under_q25) == 4 and sum(above_q75) == 1:
        #     print("4, 1")
        #     print(under_q25)
        #     print(above_q75)
        # if sum(under_q25) == 5:
        #     print(under_q25)


    # print(the_grid.house_dict[0:3])
    # plt.hist(all_distances)
    # plt.ylabel('count')
    # plt.xlabel('manhattan_distances')
    # plt.show()

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

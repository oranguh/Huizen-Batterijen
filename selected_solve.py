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
            Then it connects houses of higher output (not implemented)
        Finds houses which are only close to 2 batteries.
            Of those it selects houses with lowest output and connects them first.
            Then it connects houses of higher output (not implemented)
        Finds houses which are only close to .... etc. etc.


        BONUS:
        Once a battery is filled to capacity, do I need to make sure that the battery
        is not longer being considered for further calculations?


        idea: biggest_difference_solve()
        loop through biggest difference between optimal and second optimal connection per house
        once a battery reaches capacity pop all connection to said battery in houses and
        update the optimal and second optimal connections accordingly.
    """
    print("\n\n\n")
    print("You are now using selected_solve!")
    cap_limit = 36
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
    q0 = np.max(all_distances)

    for iqr in [q75, q50, q25]:
        for r_iqr in reversed([q75, q50, q25, q0]):
            for i in range(len(all_batteries)+1):
                # print("\nclose to only: {} far from: {}\n".format(i, (len(all_batteries) - i)))
                for index_house, house in enumerate(the_grid.house_dict):
                    connections = [house[battery] for battery in all_batteries]
                    logicals_q25 = [(r_iqr <= connect[1]) for connect in connections]
                    logicals_q75 = [(iqr >= connect[1]) for connect in connections]

                    # note that q25 returns the 'worst' connections and q75 returns the best
                    # print(sum(under_q25))
                    # print(i)
                    #  I suspect the problem is here. The indexing using i is not good.
                    # especially since I also dynamically change the length of all_batteries
                    if (sum(logicals_q75) == i) and (sum(logicals_q25) == len(all_batteries) - i):
                        # print(logicals_q25)
                        # print(logicals_q75)
                        best_connections = []
                        for j in range(len(all_batteries)):
                              best_connections += [house[all_batteries[j]]]
                        # must use numpy to index array in an easy way
                        best_connections = np.array(best_connections)
                        # print(all_batteries)
                        best = best_connections[np.argmin(best_connections[:,1]),0]


                        if the_grid.connect(best, house['position']):
                            # print("connected battery: {} with house {}".format(best, house['position']))
                            # CAUTION I am changing the list I am workin in, is that dangerous?
                            the_grid.house_dict.pop(index_house)

                            # Full battery removal
                            if the_grid.grid[best[0],best[1]].capacity_left < cap_limit:
                                all_batteries.remove('distance_to_' + str(best))
                        else:
                            print("Failed to connect")

    # print(the_grid.house_dict[0:3])
    # plt.hist(all_distances)
    # plt.ylabel('count')
    # plt.xlabel('manhattan_distances')
    # plt.show()
    # print(the_grid.grid[42, 3].capacity_left)
    # print(the_grid.grid[43, 13].capacity_left)
    # print(the_grid.house_dict)
    # the_grid.solve()
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

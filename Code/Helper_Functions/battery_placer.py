import itertools
from scipy.ndimage import gaussian_filter
import numpy as np
import csv
import random

# x,y = divmod(18, 8)
#
# print(x,y)
# print(len(range(1, 5)))
# for x in itertools.combinations(range(10), 5):
# # print(len(range(1, (48**2) + 1)))
#     print(x)
# x = 0
# for i in range (10):
    # print(random.randint(0, 4))
    # print(random.randint(0,1))
    # print([-1,1][random.randrange(2)])
    # x += -1
    # print(x)
def battery_placer(the_grid, SIGMA = 10):
    """
    convolves a gaussian filter onto the grid, then visualizes this as a heat map
    Setting SIGMA to a nice value is an important hyperparameter. my intuition tells me
    that the sigma should be a value which changes depending on the size of your matrix and/or
    the spread of your houses. But mainly the spread of your houses.
    Perhaps it would be interesting to calculate the standad deviation of distances
    between houses and to approximate the best sigma from that?

    combinations are crazy
    https://www.calculatorsoup.com/calculators/discretemathematics/combinations.php
    (51^2)! / (5!((51^2)-5)!
    8.1 * 10^14

    permutations are even crazier (problem d)
    https://www.calculatorsoup.com/calculators/discretemathematics/permutations.php
    PROBLEM. Permutations are crazy large 9.7 * 10^16

    Solution! Do a semi-greedy approach. Use the centroid of the matrix to calculate
    the top 2 positions for batteries. THEN use permutations -> 1.5 * 10^10

    But...still very large? Maybe do greedy top 3 with centroids, then reduce permutations
    to 6.2 * 10^6

    Greedy -> center of mass https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.ndimage.measurements.center_of_mass.html

    OR... use a greedy start configuration [12*12, 25*25, 12*37, 37*12, 37*37]
    and then use hill_climber
    """
    # determining sigma is important. A quick a dirty value is dimensions/batteries
    # 51/5 = 10

    numb_battery = 5
    battery_capacity = 1507.0
    best_heat = 99999
    Algo = "Exhaust"
    Algo = "Hill_climb"

    heatmatrix_house = np.zeros(the_grid.size)
    for housi in the_grid.house_dict:
        heatmatrix_house[housi['position'][0], housi['position'][1]] = housi['output']
    guass_heatmatrix_house = gaussian_filter(heatmatrix_house, sigma=SIGMA)

    if Algo == "Exhaust":
        for battery_perm in itertools.combinations(range(1, ((the_grid.size[0] - 1)**2) + 1), numb_battery):

            heatmatrix_battery = np.zeros(the_grid.size)
            for batteri in battery_perm:
                x,y = divmod(batteri, the_grid.size[0])
                # print(x,y)
                heatmatrix_battery[x, y] = battery_capacity

            guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA)
            heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
            score_battery_position = np.sum(np.absolute(heatmatrix_difference))

            if score_battery_position < best_heat:
                print(score_battery_position)
                best_heat = score_battery_position
                best_battery_config = heatmatrix_battery

                path = "Results/Battery_configurations/" + "test" + ".csv"
                with open(path, "w") as f:
                    writer = csv.writer(f,delimiter=':',quoting=csv.QUOTE_NONE)
                    writer.writerow(["pos		cap"])
                    for x, row in enumerate(heatmatrix_battery):
                        for y, column in enumerate(row):
                            if column == 0:
                                continue
                            else:
                                bad_format = "[" + str(x) + ", " + str(y) + "]\t" + str(column)
                                # print(bad_format)
                                writer.writerow([bad_format])

    elif Algo == "Hill_climb":
        # best_config = [[12,12], [25,25], [12,37], [37,12], [37,37]]
        best_config = [[random.randint(0, 50),random.randint(0, 50)],
                        [random.randint(0, 50),random.randint(0, 50)],
                        [random.randint(0, 50),random.randint(0, 50)],
                        [random.randint(0, 50),random.randint(0, 50)],
                        [random.randint(0, 50),random.randint(0, 50)]]

        heatmatrix_battery = np.zeros(the_grid.size)
        for position in best_config:
            heatmatrix_battery[best_config[0], best_config[1]] = battery_capacity

        guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA)
        heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
        best_heat = np.sum(np.absolute(heatmatrix_difference))

        counter = 0
        while counter < 10000:
            new_config = Battery_climber(best_config)
            # print(new_config)
            heatmatrix_battery = np.zeros(the_grid.size)
            for position in new_config:
                heatmatrix_battery[new_config[0], new_config[1]] = battery_capacity

            guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA)
            heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
            score_battery_position = np.sum(np.absolute(heatmatrix_difference))
            counter += 1
            if score_battery_position < best_heat:
                counter = 0
                best_heat = score_battery_position
                best_config = new_config
                print(best_config)
                print(best_heat)
                path = "Results/Battery_configurations/" + "SCORE:" + str(int(best_heat)) + "_SIGMA:" + str(SIGMA) + ".csv"
                with open(path, "w") as f:
                    writer = csv.writer(f,delimiter=':',quoting=csv.QUOTE_NONE)
                    writer.writerow(["pos		cap"])
                    for battery in best_config:
                        bad_format = "[" + str(battery[0]) + ", " + str(battery[1]) + "]\t" + str(1507.0)
                        # print(bad_format)
                        writer.writerow([bad_format])
    else:
        pass
    print(best_heat)
    return(best_config)

def Battery_climber(best_config):

    battery_index = random.randint(0, len(best_config)-1)
    x_or_y = random.randint(0,1)
    add_or_subtract = [-1,1][random.randrange(2)]

    if best_config[battery_index][x_or_y] == 0:
        best_config[battery_index][x_or_y] += 1
    elif best_config[battery_index][x_or_y] == 50:
        best_config[battery_index][x_or_y] -= 1
    else:
        best_config[battery_index][x_or_y] += add_or_subtract
    return best_config

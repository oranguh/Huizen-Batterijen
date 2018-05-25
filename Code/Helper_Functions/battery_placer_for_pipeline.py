import itertools
from scipy.ndimage import gaussian_filter
import numpy as np
import csv
import random
import json
import pprint
import copy

def battery_placer(house_dict, bat_comp, counter_limit = 10, inner_counter_limit = 100):
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

    numb_battery = len(bat_comp['batteries'])
    battery_capacity = bat_comp['batteries']
    best_heat = 99999
    counter_limit = 10
    inner_counter_limit = 100
    SIGMA = 51/numb_battery

    heatmatrix_house = np.zeros([51,51])
    house_cords = []
    # print(house_dict)
    for housi in house_dict:
        x = housi['position'][0]
        y = housi['position'][1]
        heatmatrix_house[x, y] = housi['output']
        house_cords.append(housi['position'])
    guass_heatmatrix_house = gaussian_filter(heatmatrix_house, sigma=SIGMA)

    # best_config = [[12,12], [25,25], [12,37], [37,12], [37,37]]
    best_config = [[random.randint(0, 50),random.randint(0, 50)] for j in range(numb_battery)]
    new_config = best_config
    heatmatrix_battery = np.zeros([51,51])

    for i, position in enumerate(best_config):
        heatmatrix_battery[position[0], position[1]] = battery_capacity[i]

    guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA, mode = 'constant')
    heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
    best_heat = np.sum(np.absolute(heatmatrix_difference))
    counter = 0
    inner_counter = 0
    duplicate = True
    while counter < counter_limit and duplicate:
        if inner_counter > inner_counter_limit:
            new_config = Battery_climber(best_config, house_cords)
            inner_counter = 0
            counter += 1
        else:
            # print("searching")
            new_config = Battery_climber(new_config, house_cords)
            inner_counter += 1
        # print(new_config)
        heatmatrix_battery = np.zeros([51,51])
        for i, position in enumerate(new_config):
            heatmatrix_battery[position[0], position[1]] = battery_capacity[i]

        guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA, mode = 'constant')
        # print(np.sum(guass_heatmatrix_battery) , np.sum(guass_heatmatrix_house))
        heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
        score_battery_position = np.sum(np.absolute(heatmatrix_difference))
        if score_battery_position < best_heat:
            if check_overlap(best_config, house_cords) or check_unique(best_config):
                # print("Overlap!")
                # print(check_overlap(best_config, house_cords))
                continue
            else:
                duplicate = False
                # print("no overlaps!")
                counter = 0
                best_heat = score_battery_position
                best_config = new_config
                # print(best_config)
                # print(best_heat)

    bat_comp['bat_positions'] = best_config
    bat_comp['heatmap_score'] = best_heat
    return(bat_comp)

def Battery_climber(config, house_cords):

    battery_index = random.randint(0, len(config)-1)
    x_or_y = random.randint(0,1)
    add_or_subtract = [-1,1][random.randrange(2)]

    if config[battery_index][x_or_y] <= 0:
        config[battery_index][x_or_y] += 1
    elif config[battery_index][x_or_y] >= 50:
        config[battery_index][x_or_y] -= 1
    else:
        config[battery_index][x_or_y] += add_or_subtract
    duplo = check_unique(config)
    if duplo:
        for item in config:
            if item == duplo:
                if item[0] > 25:
                    item[0] -= 1
                else:
                    item[0] += 1
            break
    return config

def check_unique(listed):
    checked = []
    for i in listed:
        if i in checked:
            # print(listed)
            return i
        checked.append(i)
    return None

def check_overlap(listed, house_cords):
    overlaps = []
    for i in listed:
        if i in house_cords:
            # print(listed)
            overlaps.append(i)
    if overlaps:
        return i
    else:
        return None

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
    counter_limit = 100
    inner_counter_limit = 100
    SIGMA = 10

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
    new_config = [[random.randint(0, 50),random.randint(0, 50)] for j in range(numb_battery)]
    heatmatrix_battery = np.zeros([51,51])

    guass_heatmatrix_battery = heatmatrix_batteries(new_config, battery_capacity)

    heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
    best_heat = np.sum(np.absolute(heatmatrix_difference))
    counter = 0
    inner_counter = 0
    duplicate = True
    while counter < counter_limit or duplicate:
        if inner_counter > inner_counter_limit:
            if duplicate:
                new_config = Battery_climber(new_config, house_cords)
            else:
                new_config = Battery_climber(best_config, house_cords)
            inner_counter = 0
            counter += 1
        else:
            # print("searching")
            new_config = Battery_climber(new_config, house_cords)
            inner_counter += 1
        # print(new_config)
        guass_heatmatrix_battery = heatmatrix_batteries(new_config, battery_capacity)

        # print(np.sum(guass_heatmatrix_battery) , np.sum(guass_heatmatrix_house))
        heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
        score_battery_position = np.sum(np.absolute(heatmatrix_difference))
        if score_battery_position < best_heat:
            if check_overlap(new_config, house_dict):
                # print("Overlap!")
                # print(check_overlap(best_config, house_cords))
                continue
            elif check_unique(new_config):
                # print("nounique")
                continue
            else:
                # print(check_unique(new_config), check_overlap(new_config, house_dict))
                # print("not overlap")
                duplicate = False
                # print("no overlaps!")
                counter = 0
                best_heat = score_battery_position
                best_config = copy.deepcopy(new_config)

                bat_comp['bat_positions'] = copy.deepcopy(best_config)
                bat_comp['heatmap_score'] = best_heat

    # for i in best_config:
    #     for j in house_dict:
    #         if i == j["position"]:
    #             print(i, j["position"])
    # print(duplicate)
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
            return True
        checked.append(i)
    return None

def check_overlap(listed, house_dict):
    for i in listed:
        for j in house_dict:
            if i == j["position"]:
                return True
    else:
        return None

def heatmatrix_batteries(new_config, battery_capacity):

    heatmatrix_battery = np.zeros([51,51])
    heatmatrix_battery_450 = np.zeros([51,51])
    heatmatrix_battery_900 = np.zeros([51,51])
    heatmatrix_battery_1800 = np.zeros([51,51])
    for i, position in enumerate(new_config):
        if battery_capacity[i] == 450:
            default = False
            heatmatrix_battery_450[position[0], position[1]] = battery_capacity[i]
        elif battery_capacity[i] == 900:
            default = False
            heatmatrix_battery_900[position[0], position[1]] = battery_capacity[i]
        elif battery_capacity[i] == 1800:
            default = False
            heatmatrix_battery_1800[position[0], position[1]] = battery_capacity[i]
        elif battery_capacity[i] > 1500 and battery_capacity[i] < 1510:
            default = True
            heatmatrix_battery[position[0], position[1]] = battery_capacity[i]
        else:
            print("unknown battery type")
            return False
        heatmatrix_battery[position[0], position[1]] = battery_capacity[i]

    if default:
        guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=10, mode = 'constant')
        return(guass_heatmatrix_battery)
    else:
        guass_heatmatrix_battery_450 = gaussian_filter(heatmatrix_battery_450, sigma=3, mode = 'constant')
        guass_heatmatrix_battery_900 = gaussian_filter(heatmatrix_battery_900, sigma=6, mode = 'constant')
        guass_heatmatrix_battery_1800 = gaussian_filter(heatmatrix_battery_1800, sigma=12, mode = 'constant')
        guass_heatmatrix_battery = np.add(guass_heatmatrix_battery_450,guass_heatmatrix_battery_900,guass_heatmatrix_battery_1800)
        # print(guass_heatmatrix_battery)
        # return(False)
        return(guass_heatmatrix_battery)

import itertools
from scipy.ndimage import gaussian_filter
import numpy as np
import csv
import random
import json
import pprint
import copy

def battery_placer(the_grid, bat_comp):
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
    scatterplot_list = []
    numb_battery = len(bat_comp['batteries'])
    # scatterplot_list = np.array([])
    battery_capacity = bat_comp['batteries']
    best_heat = 99999
    counter_limit = 100
    inner_counter_limit = 100
    SIGMA = 51/numb_battery
    SIGMAHOUSE = 2.35
    SIGMAHOUSE = 5

    heatmatrix_house = np.zeros(the_grid.size)
    house_cords = []
    for housi in the_grid.house_dict:
        heatmatrix_house[housi['position'][0], housi['position'][1]] = housi['output']
        house_cords.append(housi['position'])
    guass_heatmatrix_house = gaussian_filter(heatmatrix_house, sigma=SIGMAHOUSE, mode = 'constant')

    best_config = [[random.randint(0, 50),random.randint(0, 50)] for j in range(numb_battery)]
    new_config = best_config
    heatmatrix_battery = np.zeros(the_grid.size)

    guass_heatmatrix_battery = heatmatrix_batteries(the_grid, new_config, battery_capacity)

    heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
    best_heat = np.sum(np.absolute(heatmatrix_difference))
    counter = 0
    inner_counter = 0
    duplicate = True
    while (counter < 10000 or duplicate):
        # print("hey")
        if inner_counter > 1000:
            new_config = Battery_climber(best_config, house_cords)
            inner_counter = 0
            counter += 1
        else:
            # print("searching")
            new_config = Battery_climber(new_config, house_cords)
            inner_counter += 1
        # print(new_config)
        guass_heatmatrix_battery, heatmatrix_battery  = heatmatrix_batteries(the_grid, new_config, battery_capacity)


        # print(np.sum(guass_heatmatrix_battery) , np.sum(guass_heatmatrix_house))
        heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)
        score_battery_position = np.sum(np.absolute(heatmatrix_difference))
        if score_battery_position < best_heat:
            if check_overlap(new_config, house_cords) or check_unique(new_config):
                # print("Overlap!")
                # print(check_overlap(best_config, house_cords))
                continue
            else:
                matrices_for_vis = [copy.deepcopy(heatmatrix_battery),
                                    copy.deepcopy(guass_heatmatrix_battery),
                                    copy.deepcopy(heatmatrix_house),
                                    copy.deepcopy(guass_heatmatrix_house)]
                duplicate = False
                counter = 0
                best_heat = score_battery_position
                best_config = copy.deepcopy(new_config)
                print(best_config)
                print(best_heat)
                bat_comp['bat_positions'] = copy.deepcopy(best_config)
                bat_comp['heatmap_score'] = best_heat
                for i in best_config:
                    for j in the_grid.house_dict:
                        if i == j["position"]:
                            print(i, j["position"])
                # path = "Results/Battery_configurations/" + "SCORE_" + str(int(best_heat)) + "_SIGMA_" + str(SIGMA) + ".csv"
                path = "Results/Battery_configurations/" + "BESTSCORE" + "_SIGMA_relative.csv"
                with open(path, "w") as f:
                    writer = csv.writer(f,delimiter=':',quoting=csv.QUOTE_NONE)
                    writer.writerow(["pos		cap"])
                    for batteris in best_config:
                        bad_format = "[" + str(batteris[0]) + ", " + str(batteris[1]) + "]\t" + str(1507.0)
                        # print(bad_format)
                        writer.writerow([bad_format])

                battery_dict_format = []
                for perbattery in best_config:
                    battery_dict_format.append({'position': perbattery, 'capacity': 1507.0})

                # print(scatterplot_list)
                scatterplot_list.append({"heatscore": best_heat, "battery_dict": copy.deepcopy(battery_dict_format), "lowerbound": 0, "siman_gridscore": 0})
    # print(scatterplot_list)
    scatterplot_data = {"DATAMETA": {"DATA": scatterplot_list, "SIGMA": "relative", "R2": 0, "regression": 0}}
    path = "Results/Battery_configurations/" + "scatterplotdata_sigma_relative.json"
    with open(path, 'w') as jsonfile:
        json.dump(scatterplot_data, jsonfile)
    # print(best_heat)


    return(bat_comp, matrices_for_vis)

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

def heatmatrix_batteries(the_grid, new_config, battery_capacity):

    heatmatrix_battery = np.zeros(the_grid.size)
    heatmatrix_battery_450 = np.zeros(the_grid.size)
    heatmatrix_battery_900 = np.zeros(the_grid.size)
    heatmatrix_battery_1800 = np.zeros(the_grid.size)
    for i, position in enumerate(new_config):
        # print(battery_capacity[i])
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
        guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=5, mode = 'constant')
        return(guass_heatmatrix_battery, heatmatrix_battery)
    else:
        guass_heatmatrix_battery_450 = gaussian_filter(heatmatrix_battery_450, sigma=3, mode = 'constant')
        guass_heatmatrix_battery_900 = gaussian_filter(heatmatrix_battery_900, sigma=4.5, mode = 'constant')
        guass_heatmatrix_battery_1800 = gaussian_filter(heatmatrix_battery_1800, sigma=6, mode = 'constant')
        guass_heatmatrix_battery = np.add(guass_heatmatrix_battery_450,guass_heatmatrix_battery_900, heatmatrix_battery_1800)
        guass_heatmatrix_battery = np.add(guass_heatmatrix_battery,guass_heatmatrix_battery_1800)
        # heatmatrix_battery = np.add(heatmatrix_battery_450,heatmatrix_battery_900,heatmatrix_battery_1800)
        # print(guass_heatmatrix_battery)
        return(guass_heatmatrix_battery, heatmatrix_battery)

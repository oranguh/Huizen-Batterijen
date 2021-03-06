import sys
import numpy as np
from scipy import stats
import colorama
from termcolor import cprint
import matplotlib.pyplot as plt
import json
from smart_grid import SmartGrid
from read_data import read_data
from heat_map import heat_map
import csv

# sys.path.append('Code/Helper_Functions')
sys.path.append('../Algorithms')
# sys.path.append('Data/')
# sys.path.append('Results/')
from random_solve import random_solve
from Hill_Climber_random_for_pipeline import Hillclimber
from siman_for_pipeline import Simulated_annealing

def main():
    """
        Creates a scatterplot of the heatmap. Creates 2 subplots, one comparing
        the heatmaps_scores with grid_scores from simulated annealing
        the other comparing grid_lowerbounds with grid_scores from simulated annealing


    """
    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'
    houses, unused = read_data(house_path, battery_path)
    # print(unused)
    best_score = 999999

    with open("../../Results/Battery_configurations/scatterplotdata_sigma_relative.json") as f:
        parsed_data = json.load(f)

    for i, batter_positions in enumerate(parsed_data['DATAMETA']['DATA']):

        batteries = batter_positions['battery_dict']

        scatterwijk = SmartGrid(51,51)
        for element in houses:
            scatterwijk.create_house(element['position'], element['output'])
        for element in batteries:
            scatterwijk.create_battery(element['position'], element['capacity'])

        # pretty sure some houses and batteries overlap each other @.@ so much to do
        scatterwijk.add_house_dictionaries(houses)
        scatterwijk.add_battery_dictionaries(batteries)

        scatterwijk.house_dict_with_manhattan_distances()
        # print(scatterwijk.house_data)
        scatterwijk.get_lower_bound()
        # print(type(scatterwijk.lower_bound))
        parsed_data['DATAMETA']['DATA'][i]['lowerbound'] = scatterwijk.lower_bound

        for _ in range(10):
            scatterwijk.grid = random_solve(scatterwijk)
            if scatterwijk.grid is False:
                print("Skipping due to random taking too long")
                continue
            for _ in range(2):
                scatterwijk.house_dict_with_manhattan_distances()
                hillclimber = Hillclimber(scatterwijk.house_data, scatterwijk.battery_dict)
                while hillclimber.run():
                    pass
                for _ in range(1):
                    siman = Simulated_annealing(hillclimber.houses, hillclimber.batteries, hillclimber.combs)
                    siman.run()
                    print("Simulated Annealing: {}".format(siman.calc_cost()))
                    if (siman.calc_cost()) < best_score:
                        best_score = siman.calc_cost()
        # # scatterwijk.prettify()
        # total_cost = scatterwijk.calc_cost()
        # print("Simulated Annealing: {}".format(siman.calc_cost()))
        print("Best score: {}".format(best_score))
        # print("price of wijk random{}".format(total_cost))
        # DO SIMANNEALING HERE
        parsed_data['DATAMETA']['DATA'][i]['siman_gridscore'] = best_score

    heat = []
    lower = []
    simanscore = []
    for datapoint in parsed_data['DATAMETA']['DATA']:
        heat.append(int(datapoint['heatscore']))
        lower.append(int(datapoint['lowerbound']))
        simanscore.append(int(datapoint['siman_gridscore']) + parsed_data['DATAMETA']['battery_price'])

    slope, intercept, r_value, p_value, std_err = stats.linregress(heat, simanscore)
    print(slope, intercept, r_value, p_value, std_err)
    fit = np.polyfit(heat, simanscore, deg=1)

    parsed_data['DATAMETA']['regression'] = fit
    parsed_data['DATAMETA']['R2'] = r_value
    # print(heat, lower)
    regresion = []
    for datapointo in heat:
        regresion.append(float(fit[0]) * datapointo + fit[1])
    title = "correlation between heatmap and Simulated Annealing \n R^2 = " + str(r_value) + "\n sigma =" + str(parsed_data['DATAMETA']['SIGMA'])
    plt.figure(1)
    plt.subplot(121)
    plt.title(title)
    plt.plot(heat, regresion, color='red')
    plt.scatter(heat, simanscore, marker='+')
    plt.xlabel('Heatmap Score')
    plt.ylabel('Simulated Annealing')

    slope, intercept, r_value, p_value, std_err = stats.linregress(lower, simanscore)
    fit = np.polyfit(lower, simanscore, deg=1)
    regresion = []
    for datapointo in lower:
        regresion.append(float(fit[0]) * datapointo + fit[1])

    plt.subplot(122)
    title = "correlation between lower bound and Simulated Annealing \n R^2 = " + str(r_value)
    plt.title(title)
    plt.plot(lower, regresion, color='red')
    plt.scatter(lower, simanscore, marker='+')
    plt.xlabel('Lower Bound')
    plt.ylabel('Simulated Annealing')
    plt.show()

    # f.close()
    #
    # with open("../../Results/Battery_configurations/scatterplotdata_sigma10.json", "w") as f:
    #     json.dump(parsed_data, f)



if __name__ == "__main__":
    main()

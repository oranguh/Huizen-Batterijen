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

def main():
    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'
    houses, unused = read_data(house_path, battery_path)
    # print(unused)

    with open("../../Results/Battery_configurations/scatterplotdata_sigma10.json") as f:
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

        # parsed_data['DATAMETA']['DATA'][i]['siman_gridscore'] = 0

    heat = []
    lower = []
    for datapoint in parsed_data['DATAMETA']['DATA']:
        heat.append(int(datapoint['heatscore']))
        lower.append(int(datapoint['lowerbound']))

    slope, intercept, r_value, p_value, std_err = stats.linregress(heat, lower)
    print(slope, intercept, r_value, p_value, std_err)
    fit = np.polyfit(heat, lower, deg=1)
    parsed_data['DATAMETA']['regression'] = fit
    parsed_data['DATAMETA']['R2'] = r_value
    # print(heat, lower)
    regresion = []
    for datapointo in heat:
        regresion.append(float(fit[0]) * datapointo + fit[1])
    title = "correlation between heatmap and lower bound \n R^2 = " + str(r_value) + "\n sigma =" + str(parsed_data['DATAMETA']['SIGMA'])
    plt.title(title)
    plt.plot(heat, regresion, color='red')
    plt.scatter(heat, lower, marker='+')
    plt.xlabel('Heatmap Score')
    plt.ylabel('Lower Bound')
    plt.show()

    # f.close()
    #
    # with open("../../Results/Battery_configurations/scatterplotdata_sigma10.json", "w") as f:
    #     json.dump(parsed_data, f)


    # print(parsed_data)

if __name__ == "__main__":
    main()

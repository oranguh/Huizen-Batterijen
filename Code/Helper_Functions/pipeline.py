import json
from operator import itemgetter
import sys
from battery_placer_for_pipeline import battery_placer
from smart_grid import SmartGrid

sys.path.append('../Algorithms')
from random_solve import random_solve
from read_data import read_data


def main():

    bat_comp_path = "../../Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)

    best_4_bat_configs = sorted(parsed_data["ALL_CONFIGURATIONS"], key=itemgetter('score'))[0:4]

    for comp in best_4_bat_configs:
        houses = create_house_dict(1)
        comp = battery_placer(houses, comp, 10)
        compwijk = SmartGrid(51,51)
        battery_dict = []
        for element in houses:
            compwijk.create_house(element['position'], element['output'])
        for i,element in enumerate(comp["batteries"]):
            compwijk.create_battery(comp['bat_positions'][i], element)
            battery_dict.append({"position" : comp["bat_positions"][i], "capacity" : element})
        compwijk.add_house_dictionaries(houses)
        compwijk.add_battery_dictionaries(battery_dict)
        print("battery count according to comp: {}".format(len(comp["batteries"])))
        compwijk.calc_cost()
        compwijk.grid = random_solve(compwijk)
        compwijk.prettify()




def create_house_dict(wijk):
    battery_path = "../../Data/wijk" + str(wijk) + "_batterijen.txt"
    house_path = "../../Data/wijk" + str(wijk) +"_huizen.csv"
    houses, batteries = read_data(house_path, battery_path)
    return houses

if __name__ == "__main__":
    main()

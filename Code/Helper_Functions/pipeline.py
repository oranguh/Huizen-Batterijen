import json
from operator import itemgetter
import sys

sys.path.append('../Algorithms')
from random_solve import random_solve
from read_data import read_data

def main():

    bat_comp_path = "../../Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)

    best_4_bat_configs = sorted(parsed_data["ALL_CONFIGURATIONS"], key=itemgetter('score'))[0:4]

    for comp in best_4_bat_configs:
        comp = battery_placer(create_house_dict(1), comp, 10)

def create_house_dict(wijk):
    battery_path = "../../Data/wijk" + str(wijk) + "_batterijen.txt"
    house_path = "../../Data/wijk" + str(wijk) +"_huizen.csv"
    houses, batteries = read_data(house_path, battery_path)
    return houses

if __name__ == "__main__":
    main()

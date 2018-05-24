import json
from operator import itemgetter
import sys
from battery_placer_for_pipeline import battery_placer
from smart_grid import SmartGrid
import csv

sys.path.append('../Algorithms')
from random_solve import random_solve
from read_data import read_data
from Hill_Climber_random_for_pipeline import Hillclimber
from siman_for_pipeline import Simulated_annealing

def main():

    bat_comp_path = "../../Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)
    with open("../../Results/de_aller_beste_score_ooit.csv1", "r") as fa:
        reader = csv.reader(fa)
        for i, row in enumerate(reader):
            if i is 1:
                best_score = int(row[0])

    best_4_bat_configs = sorted(parsed_data["ALL_CONFIGURATIONS"], key=itemgetter('score'))[0:4]
    for comp in best_4_bat_configs:
        compcost = comp['cost']
        houses = create_house_dict(1)
        comp = battery_placer(houses, comp, 10)
        compwijk = create_smart_grid(houses, comp)
        for _ in range(10):
            compwijk.grid = random_solve(compwijk)
            for _ in range(10):
                compwijk.house_dict_with_manhattan_distances()
                hillclimber = Hillclimber(compwijk.house_data, compwijk.battery_dict)
                while hillclimber.run():
                    pass
                for _ in range(10):
                    siman = Simulated_annealing(hillclimber.houses, hillclimber.batteries, hillclimber.combs)
                    siman.run()
                    if (siman.calc_cost() + compcost) < best_score:
                        print(siman.calc_cost() + compcost)
                        best_score = siman.calc_cost() + compcost
                        with open("../../Results/de_aller_beste_score_ooit.json", 'w') as jsonfile:
                            json.dump({"META": {"DATA": siman.houses, "BATTERIES": siman.batteries}}, jsonfile)
                        with open("../../Results/de_aller_beste_score_ooit.csv1", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([siman.calc_cost(), {"DATA": siman.houses}])
            compwijk.get_lower_bound()



def create_house_dict(wijk):
    battery_path = "../../Data/wijk" + str(wijk) + "_batterijen.txt"
    house_path = "../../Data/wijk" + str(wijk) +"_huizen.csv"
    houses, batteries = read_data(house_path, battery_path)
    return houses

def create_smart_grid(houses, comp):
    compwijk = SmartGrid(51,51)
    battery_dict = []
    for element in houses:
        compwijk.create_house(element['position'], element['output'])
    for i,element in enumerate(comp["batteries"]):
        compwijk.create_battery(comp['bat_positions'][i], element)
        battery_dict.append({"position" : comp["bat_positions"][i], "capacity" : element})
    compwijk.battery_dict = battery_dict
    compwijk.add_house_dictionaries(houses)
    compwijk.add_battery_dictionaries(battery_dict)
    return compwijk

if __name__ == "__main__":
    main()

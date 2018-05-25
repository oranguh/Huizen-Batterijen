import json
from operator import itemgetter
import sys
import csv

sys.path.append('Code/Algorithms')
sys.path.append('Code/Helper_Functions')
from random_solve import random_solve
from read_data import read_data
from Hill_Climber_random_for_pipeline import Hillclimber
from siman_for_pipeline import Simulated_annealing
from battery_placer_for_pipeline import battery_placer
from smart_grid import SmartGrid
def main(wijk_number = 1, iteration_count = 10):
    """
    pipeline for creating a good battery composition, in good battery positions
    with good connections.

    The pipeline starts with all 26 possible battery profiles. This json dataset
    is generated using batterytype_profiles.py

    These configurations are all scored using a heatmap by a hillclimber in the
    script battery_placer_for_pipeline.py

    The 4 best scores are chosen
    First, 10 random solutions are generated using random_solve.py
    For each random solution, 10 hillclimbers are performed using Hill_Climber_random_for_pipeline.py
    For each hillclimber, 10 simulated annealings are performed usin siman_for_pipeline.py

    If a highscore is found the data is saved onto a file

    PARAMETERS:
                wijk_number: determines which wijk to use
                iteration_count: amount of times to iterate, default 10
    """
<<<<<<< HEAD
    # determine which "wijk" you are using

    wijk_number = 1
    iteration_count = 10

    wijk_number = int(input("please give wijk number: "))
    if not wijk_number in [1,2,3]:
        wijk_number = 1
        print("invalid input, using default wijk 1")

    iteration_count = int(input("please give iteration count: "))

    if iteration_count not in list(range(1,20)):
        iteration_count = 10
        print("invalid/unreasonable input using 10")
=======
>>>>>>> 7847a63771515ddea318ddc8607df24aeac1bdfb
    # load file containing all 26 battery compositions
    bat_comp_path = "Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)

    # Load the best score ever found using this pipeline
    with open("Results/de_aller_beste_score_ooit.csv1", "r") as fa:
        reader = csv.reader(fa)
        for i, row in enumerate(reader):
            if i is 1:
                best_score = int(row[0])

    # Determines the heatmap scores for the 26 battery
    for i, comp in enumerate(parsed_data["ALL_CONFIGURATIONS"]):
            houses = create_house_dict(wijk_number)
            comp = battery_placer(houses, comp, 10)
            parsed_data["ALL_CONFIGURATIONS"][i]['heatmap_score'] = comp['heatmap_score']
    # picks the best 4 configurations to loop through
    best_4_bat_configs = sorted(parsed_data["ALL_CONFIGURATIONS"], key=itemgetter('heatmap_score'))[0:4]
    for i, comp in enumerate(best_4_bat_configs):
<<<<<<< HEAD
        print("\nBattery composition: {}/{} \nBattery count: {}".format(i+1, len(best_4_bat_configs), len(comp["batteries"])))
=======
        print("Battery composition: {}/{} \n Batteries total: {}".format(i+1, len(best_4_bat_configs), len(comp["batteries"])))
>>>>>>> 7847a63771515ddea318ddc8607df24aeac1bdfb
        compcost = comp['cost']
        houses = create_house_dict(wijk_number)
        compwijk = create_smart_grid(houses, comp)
        for _ in range(iteration_count):
            compwijk.grid = random_solve(compwijk)
            if compwijk.grid is False:
                print("Skipping due to random taking too long")
                continue
            for _ in range(iteration_count):
                compwijk.house_dict_with_manhattan_distances()
                hillclimber = Hillclimber(compwijk.house_data, compwijk.battery_dict)
                while hillclimber.run():
                    pass
                for _ in range(iteration_count):
                    siman = Simulated_annealing(hillclimber.houses, hillclimber.batteries, hillclimber.combs)
                    siman.run()
                    print("simulated annealing score: {}".format(siman.calc_cost() + compcost))
                    if (siman.calc_cost() + compcost) < best_score:
                        print("NEW ALLTIME HIGHSCORE: {}".format(siman.calc_cost() + compcost))
                        best_score = siman.calc_cost() + compcost
                        with open("Results/de_aller_beste_score_ooit.json", 'w') as jsonfile:
                            json.dump({"META": {"DATA": siman.houses, "BATTERIES": siman.batteries}}, jsonfile)
                        with open("Results/de_aller_beste_score_ooit.csv1", "w") as f:
                            writer = csv.writer(f)
                            writer.writerow(["score", "configuration"])
                            writer.writerow([siman.calc_cost(), {"DATA": siman.houses}])
            compwijk.get_lower_bound()

def create_house_dict(wijk_number):
    battery_path = "Data/wijk" + str(wijk_number) + "_batterijen.txt"
    house_path = "Data/wijk" + str(wijk_number) +"_huizen.csv"
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

import json
import random
import sys
import matplotlib.pyplot as plt

sys.path.append('../../Results')
from read_data import read_data
from smart_grid import SmartGrid, SmartHouse, SmartBattery

def main():

    n_random_placements = 100000
    bat_comp_path = "../../Results/battery_compositions.json"
    with open(bat_comp_path, "r") as f:
        parsed_data = json.load(f)

    battery_comps = parsed_data["ALL_CONFIGURATIONS"]
    lowests = []
    batcompcosts = [comp["cost"] for comp in battery_comps]
    nbatterijkes = [len(comp["batteries"]) for comp in battery_comps]

    for i, comp in enumerate(battery_comps):
        placements = []
        nbatteries = len(comp["batteries"])
        for _ in range(n_random_placements):
            placement = [[random.randint(0, 50),random.randint(0, 50)] for j in range(nbatteries)]
            placements.append(placement)
        lowests.append((lowest_bound(placements) * 9) + comp["cost"])
        # lowests.append((lowest_bound(placements) * 9))
        parsed_data["ALL_CONFIGURATIONS"][i]["score"] = (lowest_bound(placements) * 9) + comp["cost"]
        # print(parsed_data)
    print(lowests)
    f.close()
    with open(bat_comp_path, "w") as fa:
        json.dump(parsed_data, fa)

    title = "number of random tries per composition: " + str(n_random_placements) +  "\n x = number of batteries, y = costs of connecting houses + costs of batteries"
    # fig, axs = plt.subplots(1, 2)
    # axs[0,0].scatter(nbatterijkes, lowests)
    # axs[0,1].scatter(batcompcosts, lowests)
    # plt.scatter(batcompcosts, lowests)
    plt.scatter(nbatterijkes, lowests)
    plt.title(title)
    plt.show()


def lowest_bound(placements):
    house_path = '../../Data/wijk1_huizen.csv'
    battery_path = '../../Data/wijk1_batterijen.txt'
    houses, batteries = read_data(house_path, battery_path)

    shortest_distance_sofar = 1000000000000
    for placement in placements:
        # moet opgeteld worden
        shortest_dist = sum([shortest_distance(house['position'], placement) for house in houses])
        # print(shortest_dist)
        if shortest_dist < shortest_distance_sofar:
            shortest_distance_sofar = shortest_dist

        return shortest_distance_sofar

def shortest_distance(house_loc, battery_locs):

    # calculates distances from 1 house to battery_locs
    min_dist = min([distance(house_loc, battery_loc) for battery_loc in battery_locs])
    return min_dist

def distance(house_loc, battery_loc):

    # Calcs distance from one house to one battery
    distance = abs(house_loc[0] - battery_loc[0]) + abs(house_loc[1] - battery_loc[1])
    return distance


if __name__ == "__main__":
    main()

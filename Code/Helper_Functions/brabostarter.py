import sys
sys.path.append('../../Code/Algorithms')
sys.path.append('../../Data')
sys.path.append('../../Results')
sys.path.append('../../Code/Helper_Functions')

from smart_grid import SmartGrid
from read_data import read_data
# from brabo_solve import node
# from brabo_solve2 import solve as solve2
from brabo_solve_new_datarep import node

def brabo_starter():
    house_path = '../../Data/wijk1_huizen.csv'
    # battery_path = '../../Data/wijk1_batterijen.txt'
    # battery_path = '../../Results/Battery_configurations/SCORE:4486_SIGMA:10.csv'
    battery_path = '../../Results/Battery_configurations/leuknaampjes.csv'

    houses, batteries = read_data(house_path, battery_path, True)

    max_x = max([dic['position'][0] for dic in houses] +
                [dic['position'][0] for dic in batteries]) + 1
    max_y = max([dic['position'][1] for dic in houses] +
                [dic['position'][1] for dic in batteries]) + 1

    wijk1 = SmartGrid(max_x,max_y)
    wijk1.add_house_dictionaries(houses)
    wijk1.add_battery_dictionaries(batteries)
    houses = wijk1.house_dict_with_manhattan_distances()


    print(houses)
    root = node(batteries, houses, 5000000)
    root.solve()
    print("klaar")

def main():
    brabo_starter()

if __name__ == "__main__":
    main()

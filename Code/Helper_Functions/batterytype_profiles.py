import copy
import json
"""
Basically what we want is all the permutations for battery combinations:
The batteries we can use are as follows:
            cap     cost
PowerStar 	450 	900
Imerse-II 	900 	1350
Imerse-III 	1800 	1800

Note: all caps keep increasing by factor 2. Furthermore, the total output of the
grid is 7500. If we divide 7500 by 450 we get 16.66. Therefore, we always require
17 of the smallest battery.

In other words, we will ALWAYS use at least 1 small battery.

Say we define powerstart to be of value 1, Imerse-II to be of value 2, Imerse-III
to be of value 4. We redefine the problem as follows:

How many combinations/partitions of 16 are there where we only use the integers
1,2,4.

This problem can be re-imagined by using a square of size 4x4 (16) where
we try to fit smaller squares of 1x1, 2x2, and rectangles of 2x1.

All combinations have an associated cost to them, which is obtained by summing
the batteries respective costs.

Here I simply use a recursive algorithm to find all partitions of batteries
and their associated costs. These partitions will then be evaluated using the
battery_placer(). We can then plot the score from the battery_placer with the
cost of the battery combination.

From there we can find which combination with which battery position is most optimal.

"""
def main():
    forbidden = set([3,5,6,7,8,9,10,11,12,13,14,15,16])
    part_sets = partition(16)
    part_sets_copy = copy.deepcopy(part_sets)
    accepted_list = []

    for part_set in part_sets:
        if forbidden.intersection(part_set):
            part_sets_copy.remove(part_set)
    part_sets_copy = list(part_sets_copy)
    for setsies in part_sets_copy:
        dict_of_set = {"batteries": [], "cost": 0, "score": 0}
        for battery in list(setsies):
            if battery == 4:
                dict_of_set["batteries"].append(1800)
                dict_of_set["cost"] += 1800
            elif battery == 2:
                dict_of_set["batteries"].append(900)
                dict_of_set["cost"] += 1350
            elif battery == 1:
                dict_of_set["batteries"].append(450)
                dict_of_set["cost"] += 900
            else:
                print("ERROR")
        accepted_list.append(dict_of_set)

    accepted_list = {"ALL_CONFIGURATIONS":accepted_list}
    with open("../../Results/battery_compositions.json", 'w') as jsonfile:
        json.dump(accepted_list, jsonfile)
    print(accepted_list)


def partition(number):
     answer = set()
     answer.add((number, ))
     for x in range(1, number):
         for y in partition(number - x):
             answer.add(tuple(sorted((x, ) + y)))
     return answer

if __name__ == "__main__":
    main()

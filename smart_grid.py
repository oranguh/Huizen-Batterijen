import numpy as np
from simple_solve import *
from selected_solve import *
import colorama
from termcolor import cprint

class SmartGrid:
    """
        things to add?
        .buckets oplossing
        .calcost + validity --> +optie loggen
        .visualisatie:kleuren/nummers + x-as
        .check_validity()
        .visualize_wires()?
        .disconect --> update dict!!!!
        .hillclimb
        .move --> batterijkes (let op de dict!)
    """
    def __init__(self, range_x, range_y):
        """ user inputs ranges to define the matrix dimenions """

        # Creates numpy matrix where the elements can be anything i.e. objects
        self.grid = grid_matrix = np.empty((range_x, range_y), dtype="object")

        self.size = self.grid.shape
        self.house_count = 0
        self.battery_count = 0

    def __str__(self):
        """ print the grid with objects and its not pretty"""
        return str(self.grid)

    def __repr__(self):
        """ prints something ??? """

    def add_house_dictionaries(self, house_dict):
        """ Adds the whole dictionary for easy access in other functions
            dictionary has keys:
                                position: [x,y]
                                output: (value)
        """
        self.house_dict = house_dict

    def add_battery_dictionaries(self, battery_dict):
        """ Adds the whole dictionary for easy access in other functions
            dictionary has keys:
                                position: [x,y]
                                capacity: (value)
        """
        self.battery_dict = battery_dict

    def create_house(self, position, output):
        """ creates house object at position [x,y] with output
            (e.g. wijk1.create_house([2,3], 500))

        """
        self.position = position
        self.output = output
        self.house_count += 1

        self.grid[self.position[0], self.position[1]] = SmartHouse(self.position, self.output, self.house_count)

    def create_battery(self, position, capacity):
        """ creates battery object at position [x,y] with capacity (float)

        """
        self.position = position
        self.capacity = capacity
        self.battery_count += 1

        self.grid[self.position[0], self.position[1]] = SmartBattery(self.position, self.capacity, self.battery_count)

    def check_validity():
        """ TODO Checks whether the smart_grid is fully connected """
        pass

    def calc_cost(self):
        """ Calculates the cost of the SmartGrid by looping through every elemeny
            for batteries it uses battery.price.
            For connected houses it calculates the manhattan distance and multiplies by 9
        """
        total_cost = 0
        for row in self.grid:
            for element in row:
                if element is None:
                    continue
                if isinstance(element, SmartBattery):
                    total_cost += element.price
                if isinstance(element, SmartHouse):
                    if element.battery_connect is None:
                        continue
                    diff_x = abs(element.position[0] - element.battery_loc[0])
                    diff_y = abs(element.position[1] - element.battery_loc[1])

                    total_cost += ((diff_x + diff_y) * 9)

        return total_cost


    def connect(self, pos_battery, pos_house):
        """ Updates the capacity of the battery and the battery_connect of the house
            (usage: wijk1.connect([42, 3], [10, 27]))

        """

        # Checks whether the house is already connected
        if not self.grid[pos_house[0], pos_house[1]].battery_connect is None:
            print("house already connected to grid")
            return False

        # Checks whether battery has enough capacity left
        if self.grid[pos_house[0], pos_house[1]].output > self.grid[pos_battery[0], pos_battery[1]].capacity_left:
            print("house requires {} capacity. Battery cap at: {}".format(
            self.grid[pos_house[0], pos_house[1]].output,
            self.grid[pos_battery[0], pos_battery[1]].capacity_left))
            return False

        id = self.grid[pos_battery[0], pos_battery[1]].battery_id
        output = self.grid[pos_house[0], pos_house[1]].output

        self.grid[pos_battery[0], pos_battery[1]].capacity_update(output)
        self.grid[pos_house[0], pos_house[1]].battery_connect = id
        self.grid[pos_house[0], pos_house[1]].battery_loc = pos_battery
        return True


    def solve(self, algorithm = 'simple'):
        """ Solves the grid using an algorithm, default is simple
            solve takes in the whole SmartGrid object and returns a 'solved' grid

        """

        if algorithm is 'simple':
            self.grid = simple_solve(self)

        elif algorithm is 'selected_solve':
            self.grid = selected_solve(self)

        elif algorithm is 'ietsludieks':
            pass

        else:
            print("Unknown algorithm")

    def prettify(self):
        """ makes a pretty print version"""

        for i,row in enumerate(self.grid):
            # if i is 0:
            #     print("  ", end = "")
            #     for numb in range(51):
            #         print("{:2}".format(numb), end = "")
            #     print()
            print("{:2}| ".format(i), end = "")
            for element in row:
                if element is None:
                    print('  ', end = "")
                if isinstance(element, SmartBattery):
                    cprint("B ", "yellow", end = "")
                if isinstance(element, SmartHouse):
                    if element.battery_connect is None:
                        cprint("H ", "red", end = "")
                    else:
                        cprint("H ", "green", end = "")
            print('| {:2}'.format(i,))

    def house_dict_with_manhattan_distances(self):
        """
            updates the house_dict to contain the manhattan distances to each battery

            the items are created as: {'distance_to_[x,y]':[[x, y], <distance>]}
            where x,y are the coordinates of the battery
        """

        # iterate through every battery
        for battery in self.battery_dict:
            battery_pos = battery['position']

            # iterate through every item in list of dictionary
            for i,house in enumerate(self.house_dict):
                key_string = 'distance_to_' + str(battery_pos)
                house_pos = house['position']

                # update dict with manhattan distances
                self.house_dict[i][key_string] = [
                battery_pos,
                abs(house_pos[0] - battery_pos[0]) +
                abs(house_pos[1] - battery_pos[1])]

    def cap_left(self):
        """ """

        bat_cap_left = [self.grid[dict_element['position'][0], dict_element['position'][1]].capacity_left for dict_element in self.battery_dict]
        print(bat_cap_left)

class SmartHouse:

    def __init__(self, position,  output, house_id):
        """ makes house object with output"""
        self.position = position
        self.output = output
        self.house_id = house_id
        self.battery_connect = None
        self.battery_loc = None


class SmartBattery:

    def __init__(self, position, capacity, battery_id):
        """ makes battery object with capacity"""
        self.position = position
        self.capacity = capacity
        self.battery_id = battery_id
        self.capacity_left = self.capacity

        if self.capacity is 450:
            self.name = "Powerstar"
            self.price = 900
        elif self.capacity is 900:
            self.name = "Imerse-II"
            self.price = 1350
        elif self.capacity is 1800:
            self.name = "Imerse-III"
            self.price = 1800
        else:
            self.name = "Defeault"
            self.price = 5000

    def capacity_update(self, output):
        """ Updates the capacity_left of the battery"""
        self.capacity_left -= output



# class smart_cable():
#
#     def __init__(self, number_of_cables):
#
#         pass
#     pass

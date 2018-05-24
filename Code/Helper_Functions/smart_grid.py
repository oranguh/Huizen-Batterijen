import numpy as np
import colorama
from termcolor import cprint

# from simple_solve import *
# from selected_solve import selected_solve
# from simple_solve2 import *
# from simple_solve3 import *
# from random_solve import *


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
        self.grid = np.empty((range_x, range_y), dtype="object")

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

    def check_validity(self):
        """ Checks validity of grid

        """
        self.validity = True
        for row in self.grid:
            for element in row:
                if element is None:
                    continue
                if isinstance(element, SmartBattery):
                    if element.capacity_left < 0:
                        self.validity = False
                        return False
                if isinstance(element, SmartHouse):
                    if element.battery_connect is None:
                        self.validity = False
                        return False
        self.validity = True
        return True

    def calc_cost(self):
        """ Calculates the cost of the SmartGrid by looping through every elemeny
            for batteries it uses battery.price.
            For connected houses it calculates the manhattan distance and multiplies by 9
        """
        houses = 0
        batteries = 0
        total_cost = 0
        for row in self.grid:
            for element in row:
                if element is None:
                    continue
                if isinstance(element, SmartBattery):
                    total_cost += element.price
                    batteries += 1
                if isinstance(element, SmartHouse):
                    houses += 1
                    if element.battery_connect is None:
                        continue
                    diff_x = abs(element.position[0] - element.battery_loc[0])
                    diff_y = abs(element.position[1] - element.battery_loc[1])

                    total_cost += ((diff_x + diff_y) * 9)
        # print("houses: {}\nbatteries: {}".format(houses, batteries))
        return total_cost


    def connect(self, pos_battery, pos_house, VIS = False):
        """ Updates the capacity of the battery and the battery_connect of the house
            (usage: wijk1.connect([42, 3], [10, 27]))

        """

        # Checks whether the house is already connected
        if not self.grid[pos_house[0], pos_house[1]].battery_connect is None:
            if VIS:
                print("house already connected to grid")
            return False

        # Checks whether battery has enough capacity left
        if self.grid[pos_house[0], pos_house[1]].output > self.grid[pos_battery[0], pos_battery[1]].capacity_left:
            if VIS:
                print("house {} requires {} capacity. Battery {} cap'd at: {}".format(
                [pos_house[0], pos_house[1]],
                self.grid[pos_house[0], pos_house[1]].output,
                [pos_battery[0], pos_battery[1]],
                self.grid[pos_battery[0], pos_battery[1]].capacity_left))
            return False

        id = self.grid[pos_battery[0], pos_battery[1]].battery_id
        output = self.grid[pos_house[0], pos_house[1]].output

        self.grid[pos_battery[0], pos_battery[1]].capacity_update(output, True)
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

        elif algorithm is 'simple_solve3':
            self.grid = simple_solve3(self)

        elif algorithm is 'random_solve':
            self.grid = random_solve(self)

        else:
            print("Unknown algorithm")

    def prettify(self):
        """ makes a pretty print version"""

        for i,row in enumerate(self.grid):
            if i is 0:
                print("   ", end = "")
                for numb in range(51):
                    print("{:3}".format(numb), end = "")
                print()
            print("{:3}| ".format(i), end = "")
            for element in row:
                if element is None:
                    print('   ', end = "")
                if isinstance(element, SmartBattery):
                    cprint(" B ", "yellow", end = "")
                if isinstance(element, SmartHouse):
                    if element.battery_connect is None:
                        cprint(" H ", "red", end = "")
                    else:
                        cprint(" H ", "green", end = "")
            print('| {:3}'.format(i,))

        print("   ", end = "")
        for numb in range(51):
            print("{:3}".format(numb), end = "")
        print()

    def house_dict_with_manhattan_distances(self):
        """
            updates the house_dict to contain the manhattan distances to each battery * cost
            [[cost to battery1, cost to battery2, ... , cost to battery n, connected to battery, output][...]]

            the items are created as: {'distance_to_[x,y]':[[x, y], <distance>]}
            where x,y are the coordinates of the battery
        """
        self.house_data = []
        for i, house in enumerate(self.house_dict):
            self.house_data.append([])
            # print(house["output"])
            for j, battery in enumerate(self.battery_dict):

                self.house_data[i].append((abs(house["position"][0] - battery["position"][0]) +
                abs(house["position"][1] - battery["position"][1])) * 9)
            self.house_data[i].append(None)
            self.house_data[i].append(house["output"])

        for i,element in enumerate(self.house_dict):
            # print("hoi")
            # print(self.grid[element['position'][0],element["position"][1]].battery_connect)
            self.house_data[i][-2] = self.grid[element['position'][0],element["position"][1]].battery_connect - 1
        return(self.house_data)

    def cap_left(self):
        """
            Calculates the cost of this grid
        """

        self.bat_cap_left = [self.grid[dict_element['position'][0], dict_element['position'][1]].capacity_left for dict_element in self.battery_dict]
        # print(self.bat_cap_left)


    def disconnect(self, pos_house):
        """ disconnects the house and restores the batteries capacity_left"""

        # checks if house is connected
        if self.grid[pos_house[0], pos_house[1]].battery_connect is None:
            return False

        # gets the output and the position of the house of the battery
        output = self.grid[pos_house[0], pos_house[1]].output
        bat_pos = self.grid[pos_house[0], pos_house[1]].battery_loc

        # updates the house and battery
        self.grid[pos_house[0], pos_house[1]].battery_connect = None
        self.grid[pos_house[0], pos_house[1]].battery_loc = None
        self.grid[bat_pos[0]][bat_pos[1]].capacity_update(output, False)

        print("disconnected battery: {} with house {}".format(bat_pos, pos_house))

    def get_lower_bound(self):
        """ determines lower bound of the grid configuration
        """
        self.lower_bound = 0
        for bat in self.battery_dict:
            if (bat['capacity'] == 1507.0):
                self.lower_bound += 5000
            elif (bat['capacity'] == 450):
                self.lower_bound += 900
            elif (bat['capacity'] == 900):
                self.lower_bound += 1350
            elif (bat['capacity'] == 1800):
                self.lower_bound += 1800
            else:
                print("unknown battery type")
        if self.house_data == None:
            print("Missing self.house_data")
            pass
        else:
            # print("done! test")
            # print(len(self.house_data))
            for house in self.house_data:
                shortest_cable_cost = 99999
                for cable_cost in house[0:-2]:
                    # print(battery_distance)
                    if cable_cost < shortest_cable_cost:
                        shortest_cable_cost = cable_cost
                # print(shortest_cable_cost)
                # print(self.lower_bound)
                self.lower_bound += shortest_cable_cost

    def connect_from_new_structure(self, new_data_struture):
        # print(len(new_data_struture))
        if not len(new_data_struture) == 150:
            print("LIST DOES NOT CONTAIN 150 houses")

        # self.battery_dict[i]
        # self.house_dict[i]
        for i, element in enumerate(new_data_struture):
            # print(self.battery_dict[i]['position'])
            # print(element[-2])
            # print(self.house_dict[element[-2]]['position'])
            # print(i)
            self.connect(self.battery_dict[element[-2]]['position'], self.house_dict[i]['position'], True)

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

    def capacity_update(self, output, subtract):
        """ Updates the capacity_left of the battery. Subtract is True if a
            battery is connected and false if disconnected"""
        if subtract is True:
            self.capacity_left -= output
        else:
            self.capacity_left += output




# class smart_cable():
#
#     def __init__(self, number_of_cables):
#
#         pass
#     pass

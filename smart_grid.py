import numpy as np

class smart_grid():
    """ """
    def __init__(self, grid):
        """ Use must give a numpy matrix as argument """

        self.grid = grid
        if not isinstance(self.grid, np.ndarray):
            raise ValueError("Must give numpy array")

        self.size = self.grid.shape
        self.house_count = 0
        self.battery_count = 0

    def __str__(self):
        """ print the grid """
        return str(self.grid)

    def __repr__(self):
        """ prints something """


    def create_house(self, position, output):
        """ creates house object at position [x,y] with output"""
        self.position = position
        self.output = output
        self.house_count += 1

        self.grid[self.position[0], self.position[1]] = smart_house(self.position, self.output, self.house_count)

    def create_battery(self, position, capacity):
        """ creates battery object at position [x,y] with capacity (float)"""
        self.position = position
        self.capacity = capacity
        self.battery_count += 1

        self.grid[self.position[0], self.position[1]] = smart_battery(self.position, self.capacity, self.battery_count)

    def check_validity():
        """ TODO Checks whether the smart_grid is fully connected """
        pass

    def calc_cost(self):


        total_cost = 0
        for row in self.grid:
            for element in row:
                if element is None:
                    continue
                if isinstance(element, smart_battery):
                    total_cost += element.price
                if isinstance(element, smart_house):
                    if element.battery_connect is None:
                        continue
                    diff_x = abs(element.position[0] - element.battery_loc[0])
                    diff_y = abs(element.position[1] - element.battery_loc[1])

                    total_cost += ((diff_x + diff_y) * 9)

        return total_cost


    def connect(self, pos_battery, pos_house):
        """ Updates the capacity of the battery and the battery_connect of the house"""

        # Checks whether battery has enough capacity left
        if self.grid[pos_house[0], pos_house[1]].output > self.grid[pos_battery[0], pos_battery[1]].capacity_left:
            return False

        id = self.grid[pos_battery[0], pos_battery[1]].battery_id
        output = self.grid[pos_house[0], pos_house[1]].output

        self.grid[pos_battery[0], pos_battery[1]].capacity_update(output)
        self.grid[pos_house[0], pos_house[1]].battery_connect = id
        self.grid[pos_house[0], pos_house[1]].battery_loc = pos_battery
        return True

class smart_house():

    def __init__(self, position,  output, house_id):
        """ makes house object with output"""
        self.position = position
        self.output = output
        self.house_id = house_id
        self.battery_connect = None
        self.battery_loc = None


class smart_battery():

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

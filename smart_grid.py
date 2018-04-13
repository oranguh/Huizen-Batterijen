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

        self.grid[self.position[0], self.position[1]] = smart_house(self.output, self.house_count)

    def create_battery(self, position, capacity):
        """ creates battery object at position [x,y] with capacity (float)"""
        self.position = position
        self.capacity = capacity
        self.battery_count += 1

        self.grid[self.position[0], self.position[1]] = smart_battery(self.capacity, self.battery_count)

    def check_validity():
        """ TODO Checks whether the smart_grid is fully connected """
        pass

class smart_house():

    def __init__(self, output, house_id):
        """ makes house object with output"""
        self.output = output
        self.house_id = house_id
    def connected():
        """ TODO Whether the house is connected to the grid or not"""
        pass

class smart_battery():

    def __init__(self, capacity, battery_id):
        """ makes battery object with capacity"""
        self.capacity = capacity
        self.battery_id = battery_id

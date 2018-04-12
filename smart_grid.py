import numpy as np

class smart_grid():
    """ """
    def __init__(self, grid):
        """ Use must give a numpy matrix as argument """

        self.grid = grid
        if not isinstance(self.grid, np.ndarray):
            raise ValueError("Must give numpy array")

        self.size = self.grid.shape

    def __str__(self):
        """ print the grid """
        return str(self.grid)

    def __repr__(self):
        """ prints something """


    def create_house(self, position, output):
        """ creates house object at position [x,y] with output"""
        self.position = position
        self.output = output

        self.grid[self.position[0], self.position[1]] = house(self.output)

    def create_battery(self, position, capacity):
        """ creates battery object at position [x,y] with capacity (float)"""
        self.position = position
        self.capacity = capacity

        self.grid[self.position[0], self.position[0]] = battery(self.capacity)

    def check_validity():
        """ TODO Checks whether the smart_grid is fully connected """
        pass

class house():

    def __init__(self, output):
        """ makes house object with output"""
        self.output = output
    def connected():
        """ TODO Whether the house is connected to the grid or not"""
        pass

class battery():

    def __init__(self, capacity):
        """ makes battery object with capacity"""
        self.capacity = capacity

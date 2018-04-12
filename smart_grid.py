class smart_grid():
    """ """
    def __init__(self, grid = None):
        """ I have been told its better to use numpy for grids """
        self.grid = grid
        self.size = len(self.grid)


    def __str__(self):
        """ print the grid """
        return str(self.grid)

    def __repr__(self):
        """ prints something """

    def create_house(self, position, output):
        """ creates house object at position with output"""
        self.position = position
        self.output = output

        self.grid[self.position] = house(self.output)

    def create_battery(self, position, capacity):
        """ creates battery object at position with capacity"""
        self.position = position
        self.capacity = capacity

        self.grid[self.position] = battery(self.capacity)

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

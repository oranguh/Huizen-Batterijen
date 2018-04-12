class smart_grid():
    """ """
    def __init__(self, grid = []):
        """ I have been told its better to use numpy """
        self.grid = grid
        self.size = size(self.grid)


    def __str__(self):
        """ print the grid """
        return str(self.grid)

    def __repr__(self):
        """ prints something """

    def create_house(self, position, output):
        """ creates house object at position with output"""
        position = self.position
        output = self.output

        
    def create_battery(self, position, capacity):
        """ creates battery object at position with capacity"""
        position = self.position
        capacity = self.capacity

    def check_validity():
        """ Checks whether the smart_grid is fully connected """
        pass

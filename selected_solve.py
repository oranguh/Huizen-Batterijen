from smart_grid import *

def selective_solve(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid

        General idea:
        Weighted solve works by calculating the manhattan distances per house per battery.

        i.e. house_1: battery_1_dist (5), battery_2_dist (18), battery_3_dist (40)

        It then finds houses which are far from all batteries except 1.
        Of those it finds houses with low output and connects them first.
    """
    print("\n\n\n")
    print("You are now using selective_solve!")


    

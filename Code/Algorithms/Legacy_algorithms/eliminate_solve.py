# from ..Helper_Functions.smart_grid import *

def eliminate_solve(the_grid):
    """ Takes an unsolved SmartGrid object and returns a solved smart grid

        General idea:
        makes ALL possible connections between houses and batteries.
        Every connection is given a score determined by the following formula:

        score_of_connection = l*alpha + c*beta

        1: The length of the connection
        c: capacity of the battery

        alpha: weight of length
        beta: weight of connection

        then we eliminate the worst solutions, or we connect the best ones first.

        BONUS:
        I also want to make a third variable theta which considers the house's
        connections in relation to the rest of the grid. I.e. if house_A has 4
        connections which are very far away (globally speaking) and only 1 which
        is short (globally speaking). I want to make sure that the short one
        gets a higher score.
        But how to define theta correctly? I will think about it.

        score_of_connection = (l*alpha + c*beta)*(theta*house_conf)


        TODO:
        do I actually place the potential_connections or do I only score them?
        Once a house has only 1 potential_connections, should make it permanent?
    """

    return the_grid.grid

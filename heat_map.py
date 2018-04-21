from smart_grid import *
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

def heat_map(the_grid):
    """
    convolves a gaussian filter onto the grid, then visualizes this as a heat map

    """

    heatmatrix_house = np.zeros(the_grid.size)
    heatmatrix_battery = np.zeros(the_grid.size)

    for housi in the_grid.house_dict:
        heatmatrix_house[housi['position'][0], housi['position'][1]] = housi['output']


    for batteri in the_grid.battery_dict:
        heatmatrix_battery[batteri['position'][0], batteri['position'][1]] = batteri['capacity']


    guass_heatmatrix_house = gaussian_filter(heatmatrix_house, sigma=15)
    guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=15)

    fig, axs = plt.subplots(2, 2, figsize=(5, 5))
    axs[0, 0].matshow(heatmatrix_house)
    axs[1, 0].matshow(guass_heatmatrix_house)
    axs[0, 1].matshow(heatmatrix_battery)
    axs[1, 1].matshow(guass_heatmatrix_battery)

    plt.show()


    heatmatrix_difference = guass_heatmatrix_house - guass_heatmatrix_battery
    plt.matshow(heatmatrix_difference)
    plt.show()

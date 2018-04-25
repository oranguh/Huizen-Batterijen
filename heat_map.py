from smart_grid import *
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from matplotlib import style
from mpl_toolkits.mplot3d.axes3d import Axes3D

def heat_map(the_grid):
    """
    convolves a gaussian filter onto the grid, then visualizes this as a heat map
    Setting SIGMA to a nice value is an important hyperparameter. my intuition tells me
    that the sigma should be a value which changes depending on the size of your matrix and/or
    the spread of your houses. But mainly the spread of your houses.
    Perhaps it would be interesting to calculate the standad deviation of distances
    between houses and to approximate the best sigma from that?

    A quick and dirty method would be to get the average length of connections?
    """
    # I think 15 is a nice value?
    SIGMA = 15
    style.use('classic')


    heatmatrix_house = np.zeros(the_grid.size)
    heatmatrix_battery = np.zeros(the_grid.size)

    for housi in the_grid.house_dict:
        heatmatrix_house[housi['position'][0], housi['position'][1]] = housi['output']


    for batteri in the_grid.battery_dict:
        heatmatrix_battery[batteri['position'][0], batteri['position'][1]] = batteri['capacity']


    guass_heatmatrix_house = gaussian_filter(heatmatrix_house, sigma=SIGMA)
    guass_heatmatrix_battery = gaussian_filter(heatmatrix_battery, sigma=SIGMA)
    heatmatrix_difference = np.subtract(guass_heatmatrix_house,guass_heatmatrix_battery)

    # The sub plot part
    largest_val = np.max([np.max(guass_heatmatrix_battery), np.max(guass_heatmatrix_house)])

    cmap = plt.get_cmap('bwr')
    # diverging colormaps: 'spectral' 'bwr' 'seismic' 'PiYG' 'PuOr' 'RdYlGn'

    fig, axs = plt.subplots(3, 2)
    axs[0, 0].matshow(heatmatrix_house, vmin=None, vmax=None, cmap= 'Reds')
    axs[0, 1].matshow(heatmatrix_battery, vmin=None, vmax=None, cmap = 'Blues')

    im = axs[1, 0].matshow(guass_heatmatrix_house, vmin= largest_val*-1, cmap=cmap)
    axs[1, 1].matshow(guass_heatmatrix_battery *-1, vmin= largest_val*-1, vmax= largest_val, cmap=cmap)
    axs[2, 0].matshow(heatmatrix_difference, vmin= largest_val*-1, vmax= largest_val, cmap=cmap)
    axs[2, 1].matshow(heatmatrix_difference, vmin= largest_val*-1, vmax= largest_val, cmap=cmap)
    # plt.subplot_tool()
    fig.colorbar(im, ax=axs.ravel().tolist())
    plt.show()


    score_battery_position = np.sum(np.absolute(heatmatrix_difference))
    print("The penalty score for this battery configuration is: {}".format(score_battery_position))

    # 3-D subplots
    fig = plt.figure(figsize=plt.figaspect(0.5))
    ax = fig.add_subplot(2, 2, 1, projection='3d')
    plt.title("Houses gaussian smoothed")

    X = np.arange(0, 51, 1)
    Y = np.arange(0, 51, 1)
    X, Y = np.meshgrid(X, Y)

    Z = guass_heatmatrix_house
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, vmin= largest_val*-1, vmax= largest_val,
                           cmap=cmap, linewidth=0, antialiased=False)
    ax.set_zlim(largest_val*-1, largest_val)
    ax.view_init(30, 180)

    ax = fig.add_subplot(2, 2, 2, projection='3d')
    plt.title("Batteries gaussian smoothed")

    Z = guass_heatmatrix_battery*-1
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, vmin= largest_val*-1, vmax= largest_val,
                           cmap=cmap, linewidth=0, antialiased=False)
    ax.set_zlim(largest_val*-1, largest_val)
    ax.view_init(30, 180)

    ax = fig.add_subplot(2, 2, 3, projection='3d')
    plt.title("Difference between houses and batteries")

    Z = heatmatrix_difference
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, vmin= largest_val*-1, vmax= largest_val,
                           cmap=cmap, linewidth=0, antialiased=False)
    ax.set_zlim(largest_val*-1, largest_val)
    ax.view_init(30, 180)



    fig.colorbar(surf, aspect=10)
    plt.tight_layout()
    plt.show()

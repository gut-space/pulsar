import os
from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from typing import List, Sequence, Tuple
import numpy as np
from math import pi

def read_series_from_file(filename: str):
    # the data format is:
    # timestamp, az [deg], el[deg], delta [s], average noise
    az = []
    el = []
    noise = []
    with open(filename, "r+") as f:
        lines = f.readlines()
        for line in lines:
            if line[0] == '#':
                continue
            tokens = line.split(',')
            az.append(float(tokens[1])*pi/180.0)
            el.append(float(tokens[2]))
            noise.append(float(tokens[4]))
    return np.array(az), np.array(el), np.array(noise)

def draw_file(filename: str):
    pass

if __name__ == '__main__':

    # Let's make this 1080x1080 (so fitting nicely on Full HD screen)
    fig =  plt.Figure = plt.figure(figsize=[10.8, 10.8], dpi=100)
    ax =  plt.Axes = fig.add_subplot(projection="polar")

    colormap = plt.get_cmap('plasma')
    norm = mpl.colors.Normalize(0.0, 60.0)

    ax = plt.subplot(1, 1, 1, polar=True)

    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(90.0, 0)

    # TODO: show colormap: https://scipy-cookbook.readthedocs.io/items/Matplotlib_Show_colormaps.html
    # https://matplotlib.org/stable/tutorials/colors/colormaps.html
    # https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib

    for x in os.listdir():
        if x.endswith(".csv"):
            az, el, noise = read_series_from_file(x)
            print(f"Plotting data from file {x}")
            ax.scatter(az, el, c=noise, s=30, cmap=colormap, norm=norm, linewidths=5)

    plt.savefig("polar-chart.png")

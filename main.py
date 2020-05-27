import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from typing import List
from matplotlib.animation import FuncAnimation
from celluloid import Camera
import numpy as np


class FourierTransformer(object):
    def __init__(self, figures_arrays: List[np.array], n_coeffs: int):
        self.waves_x = [fig[:, 0] for fig in figures_arrays]
        self.waves_y = [fig[:, 1] for fig in figures_arrays]

        self.n_coeffs = n_coeffs
        self.space = None

    def estimate_coeffs(self, wave_x: np.array, wave_y: np.array):
        self.space =np.linspace(0, 2 * np.pi, wave_x.size)

        def estimate_c(n, wave: np.array) -> tuple:
            self.space = x = np.linspace(0, 2*np.pi, wave.size)
            d = self.space[1] - x[0]

            re = np.sum(wave * d * np.cos(n*self.space)) / np.pi
            im = np.sum(wave * d * np.sin(n*self.space)) / np.pi

            return re, im

        a = list()
        b = list()

        for i in range(-100, 100):
            a1, b1 = estimate_c(i, wave_x)
            a2, b2 = estimate_c(i, wave_y)
            a.append(a1 - b2)
            b.append(b1 + a2)

        return a, b


def read_point_from_file(file: str) -> np.array:
    with open(file, 'r') as f:
        points_str = f.read()

    return list(map(lambda x: list(map(float, x.split(','))), points_str.split()))


if __name__ == '__main__':
    fig = np.array(read_point_from_file('./apple/fig2.txt'))
    trans = FourierTransformer([fig], 100)
    cre, cim = trans.estimate_coeffs(trans.waves_x[0], trans.waves_y[0])
    #print(x_coefs)
    # here must be something like circle.plot() or not?
    fig = plt.figure(figsize=(7, 7))
    camera = Camera(fig)
    ax = plt.gca()

    # change default range so that new circles will work
    ax.set_xlim((-3000, 3000))
    ax.set_ylim((-3000, 3000))
    # (or if you have an existing figure)
    # fig = plt.gcf()
    # ax = fig.gca()
    #for a, b in zip(x_coefs):
    #    pass
    points_x = list()
    points_y = list()
    for i in np.linspace(0, 2*np.pi, 200):
        offset_x = offset_y = 0
        for j, (a, b) in enumerate(zip(cre, cim)):
            j -= len(cre) / 2

            x1 = a * np.cos(i * j)
            y1 = a * np.sin(i * j)

            circle1 = plt.Circle((offset_x, offset_y), a)
            circle1.set_edgecolor('r')
            circle1.set_facecolor('none')

            line1 = mlines.Line2D([offset_x, offset_x + x1], [offset_y, offset_y + y1], color='black')

            offset_x += x1
            offset_y += y1

            x2 = -b * np.sin(i * j)
            y2 = b * np.cos(i * j)

            circle2 = plt.Circle((offset_x, offset_y), b)
            circle2.set_edgecolor('r')
            circle2.set_facecolor('none')

            line2 = mlines.Line2D([offset_x, offset_x + x2], [offset_y, offset_y + y2], color='black')

            offset_x += x2
            offset_y += y2

            ax.add_artist(circle1)
            ax.add_artist(circle2)
            ax.add_line(line1)
            ax.add_line(line2)

        points_x.append(offset_x)
        points_y.append(offset_y)
        ax.plot(points_x, points_y)
        #points.append(plt.Circle((offset_x, offset_y), 1))
        #for point in points:
        #    ax.add_artist(point)

        camera.snap()
    #circle = plt.Circle((0, 15), 5, color='r')
    #ax.add_artist(circle)
    animation = camera.animate()
    animation.save('celluloid_subplots.gif', writer='imagemagick')
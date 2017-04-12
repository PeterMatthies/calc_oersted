import pyqtgraph as pg
import numpy as np


def calc_field(x_pos, z_pos, width, height, current):
    gamma = (1.2566E-6 / (4 * np.pi)) * current / (width * height)
    x1 = x_pos + width / 2
    x2 = x_pos - width / 2
    z1 = height - z_pos
    a1 = (np.power(x1, 2) + np.power(z_pos, 2)) / (np.power(x1, 2) + np.power(z1, 2))
    a2 = (np.power(x2, 2) + np.power(z_pos, 2)) / (np.power(x2, 2) + np.power(z1, 2))
    # print(gamma, x1, x2, z1, a1, a2)
    return gamma * (0.5 * x1 * np.log(a1) - 0.5 * x2 * np.log(a2) +
                    z_pos * (np.arctan(x1 / z_pos) - np.arctan(x2 / z_pos)) -
                    z1 * (np.arctan(x1 / z1) - np.arctan(x2 / z1)))

if __name__ == '__main__':

    import sys
    from PyQt5 import QtCore
    if sys.flags.interactive != 1 or not hasattr(QtCore, 'PYQT_VERSION'):
        current = 0.15
        z_pos = 90e-9
        width = 3e-6
        thickness = 25e-9

        x = np.linspace(-0.5 * width, 0.5 * width, 1000)
        y = 1000 * calc_field(x, z_pos, width, thickness, current)

        plot1 = pg.plot(x, y, symbol='x')

        pg.QtGui.QGuiApplication.exec_()
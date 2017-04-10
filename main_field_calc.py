# Oersted-field calculation
# origin of coordinate system middle bottom in the cross section of the Au wire

import sys
import numpy as np
from PyQt5 import QtGui, QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import py

class AppForm(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setWindowTitle('Oersted Field of a Rectangular Wire')

        self.create_menu()
        self.create_main_frame()
        self.create_status_bar()
        self.textbox1.setText('0.15')  # current value (A)
        self.textbox2.setText('90e-9')  # z point for which the field will be calculated
        self.textbox3.setText('3e-6')  # width of the Au wire (m)
        self.textbox4.setText('25e-9')  # thickness of the Au wire (m)
        self.on_draw()
        self.current = 0.15
        self.z_pos = 90e-9
        self.width = 3e-6
        self.thickness = 25e-9

    def save_plot(self):
        file_choices = 'PNG (*.png)|*.png'

        path = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '', file_choices))

        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def on_about(self):
        msg = """ A demo of using PyQt with matplotlib:

        * Use the matplotlib navigation bar
        * Add valuesto the text box and press Enter (or click "Draw"
        * Show or hide the grid
        * Drag the slider to modify the width of the bars
        * Save the plot to a file using the File menu
        * Click on a bar to receive an information message
        """

        QtWidgets.QMessageBox.about(self, "About the program", msg.strip())

    def on_pick(self, event):
        # the event here is of the type
        # matplotlib.backend_bases.PickEvent
        #
        # It carries lots of information, of which we're using
        # only a small amount here.
        #
        # box_points = event.artist.get_bbox().get_points()
        x, y = event.artist.get_xdata(), event.artist.get_ydata()
        ind = event.ind
        plot_point = x[ind[0]], y[ind[0]]
        msg = "You've clicked on a bar with coords:\n %s" % plot_point

        QtWidgets.QMessageBox.information(self, "Click!", msg)

    def on_draw(self):
        """Redraws the figure
        """
        self.current = float(self.textbox1.text())
        self.z_pos = float(self.textbox2.text())
        self.width = float(self.textbox3.text())
        self.thickness = float(self.textbox4.text())

        x = np.linspace(-0.5 * self.width, 0.5 * self.width, 1000)
        y = 1000 * calc_field(x, self.z_pos, self.width, self.thickness, self.current)
        # clear the axes and redraw the plot anew
        #
        self.axes.clear()
        self.axes.grid(self.grid_cb.isChecked())

        self.axes.plot(x, y, 'rx')
        # self.axes.bar(
        #     left=x,
        #     height=self.data,
        #     width=self.slider.value() / 100.0,
        #     align='center',
        #     alpha=0.44,
        #     picker=5)
        self.axes.set_xlim(-0.5 * self.width, 0.5 * self.width)
        self.axes.set_xlabel('Position across wire (m)')
        self.axes.set_ylabel(r"$B_{in\hspace{0.2} plane}$ (mT)")
        self.axes.ticklabel_format(axis='x', style='sci', scilimits=(-3, 3), useOffset=False)
        self.axes.xaxis.major.formatter._useMathText = True
        self.fig.tight_layout()
        self.canvas.draw()

    def create_main_frame(self):
        self.main_frame = QtWidgets.QWidget()
        self.main_frame.setMinimumHeight(500)

        # Create the mpl Figure and FigCanvas objects.
        # 5x4 inches, 100 dots per inch
        #
        self.dpi = 100
        self.fig = Figure((7.6, 7.0), dpi=self.dpi, tight_layout=True)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        self.axes = self.fig.add_subplot(111)

        # Bind the 'pick' event for clicking on one of the bars
        #
        self.canvas.mpl_connect('pick_event', self.on_pick)

        # Create the navigation toolbar, tied to the canvas
        #
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        #
        current_label = QtWidgets.QLabel('Current (A)')
        current_label.setMinimumWidth(50)
        self.textbox1 = QtWidgets.QLineEdit()
        self.textbox1.setMinimumWidth(50)
        self.textbox1.editingFinished.connect(self.on_draw)

        zpos_label = QtWidgets.QLabel('z position (m)')
        zpos_label.setMinimumWidth(50)
        self.textbox2 = QtWidgets.QLineEdit()
        self.textbox2.setMinimumWidth(50)
        self.textbox2.editingFinished.connect(self.on_draw)

        width_label = QtWidgets.QLabel('Width of Au wire (m)')
        width_label.setMinimumWidth(50)
        self.textbox3 = QtWidgets.QLineEdit()
        self.textbox3.setMinimumWidth(50)
        self.textbox3.editingFinished.connect(self.on_draw)

        thickness_label = QtWidgets.QLabel('Thickness of Au wire (m)')
        thickness_label.setMinimumWidth(50)
        self.textbox4 = QtWidgets.QLineEdit()
        self.textbox4.setMinimumWidth(50)
        self.textbox4.editingFinished.connect(self.on_draw)

        self.draw_button = QtWidgets.QPushButton("&Draw")
        self.draw_button.clicked.connect(self.on_draw)

        self.grid_cb = QtWidgets.QCheckBox("Show &Grid")
        self.grid_cb.setChecked(True)
        self.grid_cb.stateChanged.connect(self.on_draw)

        # slider_label = QtWidgets.QLabel('Bar width (%):')
        # self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        # self.slider.setRange(1, 100)
        # self.slider.setValue(20)
        # self.slider.setTracking(True)
        # self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        # self.connect(self.slider, QtWidgets.PYQT_SIGNAL('valueChanged(int)'), self.on_draw)
        # self.slider.valueChanged.connect(self.on_draw)

        blank_label = QtWidgets.QLabel('')
        blank_label.setMinimumWidth(100)
        #
        # Layout with box sizers
        #
        hbox1 = QtWidgets.QHBoxLayout()
        hbox2 = QtWidgets.QHBoxLayout()
        hbox3 = QtWidgets.QHBoxLayout()
        for w in [self.textbox1, self.textbox2, self.textbox3, self.textbox4]:
            hbox1.addWidget(w)
            hbox1.setAlignment(w, QtCore.Qt.AlignRight)

        for w in [current_label, zpos_label, width_label, thickness_label]:
            hbox2.addWidget(w)
            hbox2.setAlignment(w, QtCore.Qt.AlignRight)

        hbox3.addWidget(self.mpl_toolbar)
        hbox3.setAlignment(self.mpl_toolbar, QtCore.Qt.AlignVCenter)
        hbox3.addWidget(self.draw_button)
        hbox3.setAlignment(self.draw_button, QtCore.Qt.AlignVCenter)
        hbox3.addWidget(self.grid_cb)
        hbox3.setAlignment(self.grid_cb, QtCore.Qt.AlignVCenter)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(self.canvas)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.main_frame.setLayout(vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Oersted Field calculation")
        self.statusBar().addWidget(self.status_text, 1)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("&File")

        load_file_action = self.create_action("&Save plot",
                                              shortcut="Ctrl+S", slot=self.save_plot, tip='Save the plot')
        quit_action = self.create_action("&Quit", slot=self.close, shortcut="Ctrl+Q", tip='Close the application')

        self.add_actions(self.file_menu, (load_file_action, None, quit_action))

        self.help_menu = self.menuBar().addMenu("&Help")
        about_action = self.create_action("&About", shortcut="F1", slot=self.on_about, tip='About the Demo')

        self.add_actions(self.help_menu, (about_action,))

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False, signal="triggered"):
        action = QtWidgets.QAction(text, self)
        if icon is not None:
            action.setIcon(QtGui.QIcon(":/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot)
        if checkable:
            action.setCheckable(True)
        return action


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = AppForm()
    form.show()
    app.exec_()


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


if __name__ == "__main__":
    main()
    # quit()

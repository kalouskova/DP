"""Script handling GUI for manual ECG labeling"""

__author__      = "Veronika Kalouskova"
__copyright__   = "Copyright 2024, FIT CVUT"

import math 
import sys

import matplotlib as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5 import QtWidgets, QtCore
plt.use('Qt5Agg')

import data_handler


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, data, filename, fs, seg_len, seg_num):
        super(MainWindow, self).__init__()
        self.setWindowTitle(filename)

        self.DATA = data['value']
        self.FS = fs
        self.SEG_LEN = seg_len
        self.seg_curr = seg_num

        self.dh = data_handler.DataHandler(filename, len(self.DATA), self.FS, self.SEG_LEN)
        self.create_layout()
    
    #   Keypress eventhandler for navigating the ECG signal
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.on_next()
        elif event.key() == QtCore.Qt.Key_Left:
            self.on_prev()
        event.accept()

    #   Define layout elements
    def create_layout(self):
        width, height = 8, 4
        layout = QtWidgets.QGridLayout()

        # Matplotlib canvas for the ECG signal
        self.canvas = MplCanvas(self, width, height)
        layout.addWidget(self.canvas, 0, 0, 1, 10)

        # Buttons for navigating the ECG signal
        pushbutton = QtWidgets.QPushButton('PREVIOUS')
        pushbutton.clicked.connect(self.on_prev)
        pushbutton.setFixedSize(100, 30)
        layout.addWidget(pushbutton, 1, 0)

        pushbutton = QtWidgets.QPushButton('NEXT')
        pushbutton.clicked.connect(self.on_next)
        pushbutton.setFixedSize(100, 30)
        layout.addWidget(pushbutton, 1, 9)

        # Activity type
        label = QtWidgets.QLabel('ACTIVITY :')
        layout.addWidget(label, 2, 0)

        _, activity_label = self.dh.get_activity_type()
        label = QtWidgets.QLabel(activity_label)
        layout.addWidget(label, 2, 1)

        # Radio button for artifact categorization
        label = QtWidgets.QLabel('CATEGORY :')
        layout.addWidget(label, 3, 0)

        self.radio_ok = QtWidgets.QRadioButton('OK')
        self.radio_ok.setChecked(True)
        self.radio_ok.label= 0
        self.radio_ok.toggled.connect(self.on_click)
        layout.addWidget(self.radio_ok, 3, 1)

        self.radio_artifact = QtWidgets.QRadioButton('ARTIFACT')
        self.radio_artifact.label = 1
        self.radio_artifact.toggled.connect(self.on_click)
        layout.addWidget(self.radio_artifact, 3, 2)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_plot()
        self.show()
   
    #   Redraw plot containing the ECG signal
    def update_plot(self):
        # Clear the canvas
        self.canvas.axes.cla()  

        # Plot new segment
        seg_len_pts = self.SEG_LEN * self.FS
        start = self.seg_curr * seg_len_pts
        end = start + seg_len_pts

        x = np.linspace(self.seg_curr * self.SEG_LEN, (self.seg_curr * self.SEG_LEN) + self.SEG_LEN, seg_len_pts)

        self.canvas.axes.plot(x, self.DATA[start:end], linewidth=1)
        self.canvas.axes.set_title('ECG SIGNAL - SEGMENT ' + str(self.seg_curr))
        self.canvas.axes.set_xlabel('time (s)')
        self.canvas.axes.set_ylabel('(mV)')
        self.canvas.axes.grid()

        # Trigger the canvas to update and redraw
        self.canvas.draw()

        # Update radiobutton selection
        self.update_selection()

    #   Update radiobutton selection based on data
    def update_selection(self):
        artifact = self.dh.get_artifact(self.seg_curr)

        if not artifact:
            self.radio_ok.setChecked(True)
        else:
            self.radio_artifact.setChecked(True)

    #   Handle radio button keypress
    def on_click(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.dh.set_artifact(self.seg_curr, radio_button.label)

    #   Handle next button keypress
    def on_next(self):
        if (self.seg_curr < math.floor(len(self.DATA) / (self.SEG_LEN * self.FS)) - 1):
            self.seg_curr += 1
            self.update_plot()

    #   Handle previous button keypress
    def on_prev(self):
        if (self.seg_curr > 0):
            self.seg_curr -= 1
            self.update_plot()


#   Run application loop
def run(input_data, filename, fs, seg_len, seg_num):
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow(input_data, filename, fs, seg_len, seg_num)

    app.exec_()

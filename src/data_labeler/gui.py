"""PyQt5 based GUI classes for manual ECG labeling"""

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

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=8, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.subplots_adjust(0, 0, 1, 1)
        
        self.axes = fig.add_subplot(111)
        self.axes.tick_params(left = False, labelleft = False, labelbottom = False, bottom = True, direction='in', color='blue') 

        for spine in self.axes.spines.values():
            spine.set_edgecolor('blue')

        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, app, dh, fs, seg_len, seg_num, filename):
        self.dh = dh
        self.DATA = self.dh.df_in['value']
        self.FS = fs
        self.SEG_LEN = seg_len
        self.seg_curr = seg_num

        super(MainWindow, self).__init__()

        self.setWindowTitle(filename)
        self.set_styles(app)
        self.create_layout()
    
    #   Keypress eventhandler for navigating the ECG signal
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            self.on_next()
        elif event.key() == QtCore.Qt.Key_Left:
            self.on_prev()
        elif event.key() == QtCore.Qt.Key_Space:
            self.on_toggle()
        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            sys.exit()

        event.accept()

    #   Set layout styles
    def set_styles(self, app):
        app.setStyleSheet('QLabel{color: #404040;} QPushButton{color: #404040;} QRadioButton{color: #404040;}')

    #   Draw grid separator line
    def draw_line(self, x, y, layout):
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Raised)
        layout.addWidget(line, x, y, 1, 2)

    #   Define layout elements
    def create_layout(self):
        width, height = 12, 3
        layout = QtWidgets.QGridLayout()

        # Matplotlib canvas for the ECG signal
        self.canvas = MplCanvas(self, width, height)
        layout.addWidget(self.canvas, 0, 0, 20, 10)

        # Grid separators
        self.draw_line(0, 11, layout)
        self.draw_line(3, 11, layout)
        self.draw_line(6, 11, layout)

        # Buttons for navigating the ECG signal
        pushbutton = QtWidgets.QPushButton('PREVIOUS')
        pushbutton.clicked.connect(self.on_prev)
        pushbutton.setFixedSize(100, 30)
        layout.addWidget(pushbutton, 20, 0)

        pushbutton = QtWidgets.QPushButton('NEXT')
        pushbutton.clicked.connect(self.on_next)
        pushbutton.setFixedSize(100, 30)
        layout.addWidget(pushbutton, 20, 9)

        # Activity type
        label = QtWidgets.QLabel('ACTIVITY TYPE')
        layout.addWidget(label, 1, 11, 1, 2)

        _, activity_label = self.dh.get_activity_type()
        label = QtWidgets.QLabel(activity_label)
        layout.addWidget(label, 2, 11, 1, 2)

        # Electrode type
        label = QtWidgets.QLabel('ELECTRODE TYPE')
        layout.addWidget(label, 4, 11, 1, 2)

        _, electrode_label = self.dh.get_electrode_type()
        label = QtWidgets.QLabel(electrode_label)
        layout.addWidget(label, 5, 11, 1, 2)

        # Radio button for artifact categorization
        label = QtWidgets.QLabel('CATEGORY')
        layout.addWidget(label, 7, 11)

        self.radio_1 = QtWidgets.QRadioButton('1')
        self.radio_1.label = 1
        self.radio_1.toggled.connect(self.on_click)
        layout.addWidget(self.radio_1, 8, 11)

        self.radio_2 = QtWidgets.QRadioButton('2')
        self.radio_2.label = 2
        self.radio_2.toggled.connect(self.on_click)
        layout.addWidget(self.radio_2, 9, 11)

        self.radio_3 = QtWidgets.QRadioButton('3')
        self.radio_3.label = 3
        self.radio_3.toggled.connect(self.on_click)
        layout.addWidget(self.radio_3, 10, 11)

        self.radio_4 = QtWidgets.QRadioButton('4')
        self.radio_4.label = 4
        self.radio_4.toggled.connect(self.on_click)
        layout.addWidget(self.radio_4, 11, 11)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.update_plot()
        self.show()
   
    #   Redraw plot containing the ECG signal
    def update_plot(self):
        # Clear the canvas
        self.canvas.axes.cla()  

        seg_len_pts = self.SEG_LEN * self.FS            # Length of a single segment in points
        seg_start = self.seg_curr * self.SEG_LEN        # Start of current segment in seconds
        
        start = self.seg_curr * seg_len_pts             # Start of current segment in points
        end = start + seg_len_pts                       # End of current segment in points

        # Plot new segment
        x = np.linspace(seg_start, seg_start + self.SEG_LEN, seg_len_pts)
        self.canvas.axes.plot(x, self.DATA[start:end], linewidth=0.8, color='red')

        title = 'ECG    SEGMENT ' + str(self.seg_curr + 1) + '/' + str(math.floor(len(self.DATA) / seg_len_pts))
        self.canvas.axes.text(0.01, 0.98, title, ha='left', va='top', color='blue', fontsize = 10, transform=self.canvas.axes.transAxes)
       
        self.canvas.axes.set_xlim((seg_start, seg_start + self.SEG_LEN))
        self.canvas.axes.set_ylim((max(self.DATA) + 1000, min(self.DATA) - 1000))

        # Trigger the canvas to update and redraw
        self.canvas.draw()

        # Update radiobutton selection
        self.update_selection()

    #   Update radiobutton selection based on data
    def update_selection(self):
        artifact = self.dh.get_artifact(self.seg_curr)

        if artifact == 1:
            self.radio_1.setChecked(True)
        elif artifact == 2:
            self.radio_2.setChecked(True)
        elif artifact == 3:
            self.radio_3.setChecked(True)
        elif artifact == 4:
            self.radio_4.setChecked(True)

    #   Handle radio button space keypress
    def on_toggle(self):
        if (self.radio_1.isChecked()):
            self.radio_2.setChecked(True)
        elif (self.radio_2.isChecked()):
            self.radio_3.setChecked(True)
        elif (self.radio_3.isChecked()):
            self.radio_4.setChecked(True)
        elif (self.radio_4.isChecked()):
            self.radio_1.setChecked(True)

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


class Application():

    #   Run application loop
    def __init__(self, dh, fs, seg_len, seg_num, filename):
        app = QtWidgets.QApplication(sys.argv)
        win = MainWindow(app, dh, fs, seg_len, seg_num, filename)

        app.exec_()

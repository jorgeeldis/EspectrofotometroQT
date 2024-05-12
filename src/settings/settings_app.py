from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox, QGraphicsView, QCheckBox
from ui.main_window_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGridLayout
from PyQt5 import QtGui


class SettingsWindow(QMainWindow, Ui_MainWindow):
    saveSettingsRequested = pyqtSignal(tuple)
    clearViewBoxRequested = pyqtSignal()
    
    def __init__(self, parent=None, backgroundColor=(0, 0, 0)):
        super(SettingsWindow, self).__init__(parent)
        self.setWindowTitle("Settings")
        self.graphicsView = QGraphicsView(self)
        self.backgroundColor = backgroundColor


        # Create a central widget to hold the layout and widgets
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        # Create a layout
        self.layout = QGridLayout(self.centralWidget)

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 24 points

        self.backgroundColorLabel = QLabel("Background color:")
        self.backgroundColorLabel.setFont(font)
        self.layout.addWidget(self.backgroundColorLabel, 0, 0)
        self.backgroundColorLineEdit = QLineEdit(self)
        self.backgroundColorLineEdit.setFont(font)
        self.backgroundColorLineEdit.setText(", ".join(map(str, backgroundColor)))
        self.layout.addWidget(self.backgroundColorLineEdit, 1, 0)

        # QLineEdit widgets for custom ranges
        # Placeholder text for custom ranges
        self.xRangeLineEdit = QLineEdit(self)
        self.xRangeLineEdit.setFont(font)
        self.xRangeLineEdit.setText("300, 750")  # Placeholder text for x range
        self.yRangeLineEdit = QLineEdit(self)
        self.yRangeLineEdit.setFont(font)
        self.yRangeLineEdit.setText("0, 1")      # Placeholder text for y range
        self.layout.addWidget(QLabel("Custom Range:"), 2, 0)
        self.layout.addWidget(QLabel("X Range (x1, x2):"), 3, 0)
        self.layout.addWidget(self.xRangeLineEdit, 4, 0)
        self.layout.addWidget(QLabel("Y Range (y1, y2):"), 5, 0)
        self.layout.addWidget(self.yRangeLineEdit, 6, 0)

        # Checkbox for auto-ranging
        self.autoRangeCheckBox = QCheckBox("Auto Range", self)
        self.autoRangeCheckBox.setFont(font)
        self.layout.addWidget(self.autoRangeCheckBox, 0, 1)

        # Checkbox for log mode
        self.logModeCheckBox = QCheckBox("Log Mode (Y-axis)", self)
        self.logModeCheckBox.setFont(font)
        self.layout.addWidget(self.logModeCheckBox, 1, 1)

        # Checkbox for log mode for x-axis
        self.logModeXCheckBox = QCheckBox("Log Mode (x-axis)", self)
        self.logModeXCheckBox.setFont(font)
        self.layout.addWidget(self.logModeXCheckBox, 2, 1)

        self.derivativeModeCheckBox = QCheckBox("Derivative Mode", self)
        self.derivativeModeCheckBox.setFont(font)
        self.layout.addWidget(self.derivativeModeCheckBox, 3, 1)

        self.invertGraphYCheckBox = QCheckBox("Invert Graph (y-axis)", self)
        self.invertGraphYCheckBox.setFont(font)
        self.layout.addWidget(self.invertGraphYCheckBox, 4, 1)

        self.invertGraphXCheckBox = QCheckBox("Invert Graph (x-axis)", self)
        self.invertGraphXCheckBox.setFont(font)
        self.layout.addWidget(self.invertGraphXCheckBox, 5, 1)

        self.antialiasingCheckBox = QCheckBox("Antialiasing", self)
        self.antialiasingCheckBox.setFont(font)
        self.layout.addWidget(self.antialiasingCheckBox, 6, 1)

        # Button to clear view box
        self.clearViewBoxButton = QPushButton("Clear View Box", self)
        self.clearViewBoxButton.clicked.connect(self.clearViewBoxRequested.emit)
        self.clearViewBoxButton.setFont(font)
        self.layout.addWidget(self.clearViewBoxButton)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveSettings)
        self.saveButton.setFont(font)  # Set the font for the button
        self.layout.addWidget(self.saveButton)

    def saveSettings(self):
        rgb_values = list(map(int, self.backgroundColorLineEdit.text().split(', ')))
        self.backgroundColor = tuple(rgb_values)
        auto_range = self.autoRangeCheckBox.isChecked()  # Check if auto-ranging is enabled
        x_range = tuple(map(float, self.xRangeLineEdit.text().split(',')))
        y_range = tuple(map(float, self.yRangeLineEdit.text().split(',')))
        log_mode_y = self.logModeCheckBox.isChecked()  # Check if log mode for y-axis is enabled
        log_mode_x = self.logModeXCheckBox.isChecked()  # Check if log mode for x-axis is enabled
        derivative_mode = self.derivativeModeCheckBox.isChecked()  # Check if derivative mode is enabled
        invert_mode_y = self.invertGraphYCheckBox.isChecked()
        invert_mode_x = self.invertGraphXCheckBox.isChecked()
        antialiasing = self.antialiasingCheckBox.isChecked()
        self.saveSettingsRequested.emit((self.backgroundColor, auto_range, x_range, y_range, log_mode_y, log_mode_x, derivative_mode, invert_mode_y, invert_mode_x, antialiasing))

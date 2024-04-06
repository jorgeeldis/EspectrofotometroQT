from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox, QGraphicsView, QCheckBox
from ui.main_window_ui import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal


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
        self.layout = QVBoxLayout(self.centralWidget)

        self.backgroundColorLabel = QLabel("Background color:")
        self.layout.addWidget(self.backgroundColorLabel)
        self.backgroundColorLineEdit = QLineEdit(self)
        self.backgroundColorLineEdit.setText(", ".join(map(str, backgroundColor)))
        self.layout.addWidget(self.backgroundColorLineEdit)

        # QLineEdit widgets for custom ranges
        # Placeholder text for custom ranges
        self.xRangeLineEdit = QLineEdit(self)
        self.xRangeLineEdit.setText("300, 750")  # Placeholder text for x range
        self.yRangeLineEdit = QLineEdit(self)
        self.yRangeLineEdit.setText("0, 1")      # Placeholder text for y range
        self.layout.addWidget(QLabel("Custom Range:"))
        self.layout.addWidget(QLabel("X Range (x1, x2):"))
        self.layout.addWidget(self.xRangeLineEdit)
        self.layout.addWidget(QLabel("Y Range (y1, y2):"))
        self.layout.addWidget(self.yRangeLineEdit)

        # Checkbox for auto-ranging
        self.autoRangeCheckBox = QCheckBox("Auto Range", self)
        self.layout.addWidget(self.autoRangeCheckBox)

        # Checkbox for log mode
        self.logModeCheckBox = QCheckBox("Log Mode (Y-axis)", self)
        self.layout.addWidget(self.logModeCheckBox)

        # Checkbox for log mode for x-axis
        self.logModeXCheckBox = QCheckBox("Log Mode (x-axis)", self)
        self.layout.addWidget(self.logModeXCheckBox)

        self.derivativeModeCheckBox = QCheckBox("Derivative Mode", self)
        self.layout.addWidget(self.derivativeModeCheckBox)

        self.invertGraphYCheckBox = QCheckBox("Invert Graph (y-axis)", self)
        self.layout.addWidget(self.invertGraphYCheckBox)

        self.invertGraphXCheckBox = QCheckBox("Invert Graph (x-axis)", self)
        self.layout.addWidget(self.invertGraphXCheckBox)

        self.antialiasingCheckBox = QCheckBox("Antialiasing", self)
        self.layout.addWidget(self.antialiasingCheckBox)

        # Button to clear view box
        self.clearViewBoxButton = QPushButton("Clear View Box", self)
        self.clearViewBoxButton.clicked.connect(self.clearViewBoxRequested.emit)
        self.layout.addWidget(self.clearViewBoxButton)

        # Create a save button
        self.saveButton = QPushButton("Save", self)
        self.saveButton.clicked.connect(self.saveSettings)
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

import sys
import time
import qdarktheme
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QMainWindow,
    QMessageBox,
)
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
from baseline.baseline_process import BaselineProcessor
from single.single_process import SingleProcessor
from selectwavelength.wavlength_process import get_line_value, get_absorbance
from settings.settings_app import SettingsWindow
from savedata.save_process import SaveWindow
from ui.main_window_ui import Ui_MainWindow
import pyqtgraph as pg
from PyQt5.QtWidgets import QInputDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.connectSignalsSlots()
        self.init()

        # Connect the menu signals to methods
        self.menuMain.aboutToShow.connect(self.handleMainAction)

        # Create a QAction
        self.dataAction = QtWidgets.QAction("Show Data", self)
        # Add the QAction to the "Data" menu
        self.menuData.addAction(self.dataAction)
        # Connect the QAction's triggered signal to a method
        self.dataAction.triggered.connect(self.handleDataAction)

        # Create a QAction
        self.spanActionX = QtWidgets.QAction("Select Range (X-axis)", self)
        # Add the QAction to the "Data" menu
        self.spanData.addAction(self.spanActionX)
        # Connect the QAction's triggered signal to a method
        self.spanActionX.triggered.connect(self.handleSpanActionX)

        self.backgroundColor = (0, 0, 0)

        self.btn_continuous = False

    def connectSignalsSlots(self):
        self.btnBaseline.clicked.connect(self.btnBaseline_click)
        self.btnSingle.clicked.connect(self.btnSingle_click)
        self.btnContinuous.clicked.connect(self.btnContinuous_click)
        self.btnSaveData.clicked.connect(self.btnSaveData_click)
        self.btnSettings.clicked.connect(self.btnSettings_click)
        self.btnWavelength.clicked.connect(self.btnWavelength_click)

    def init(self):
        self.scene = QGraphicsScene()

        self.pg = pg
        self.timer = pg.QtCore.QTimer()
        self.selfCalibration()

        self.timer_continue = pg.QtCore.QTimer()
        self.timer_continue.start(5)
        self.timer_continue.timeout.connect(self.timer_timeout)

    def selfCalibration(self):
        # Disable buttons
        self.btnBaseline.setDisabled(True)
        self.btnSingle.setDisabled(True)
        self.btnContinuous.setDisabled(True)
        self.btnSaveData.setDisabled(True)
        self.btnSettings.setDisabled(True)
        self.btnWavelength.setDisabled(True)
        # Simulate a button press after 3 seconds
        QTimer.singleShot(1000, self.calibrate)  # 3000 milliseconds = 3 seconds

    def calibrate(self):
        self.graphWidget.clear()
        self.baseline = BaselineProcessor(
            self.graphWidget,
            self.pg,
            self.app,
            self.timer,
            self.progressBar,
            self.db450Label,
            self.db435Label,
            self.db500Label,
            self.db550Label,
            self.db570Label,
            self.db600Label,
            self.db650Label,
            self.maxDBLabel,
            self.maxNMLabel,
            self.minDBLabel,
            self.minNMLabel,
            self.specificLabel,
            self.btnBaseline,
            self.btnSingle,
            self.btnContinuous,
            self.btnSaveData,
            self.btnSettings,
            self.btnWavelength,
        )
        self.progressBar.setProperty("value", 0)
        self.baseline.send_data("1")
        self.messageBox.setText("Calibrating...")
        time.sleep(1)  # Esperar a que el arduino se inicialice

        self.timer.timeout.connect(self.baseline.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btnBaseline_click(self):
        print("Baseline Clicked")
        self.graphWidget.clear()
        self.baseline = BaselineProcessor(
            self.graphWidget,
            self.pg,
            self.app,
            self.timer,
            self.progressBar,
            self.db450Label,
            self.db435Label,
            self.db500Label,
            self.db550Label,
            self.db570Label,
            self.db600Label,
            self.db650Label,
            self.maxDBLabel,
            self.maxNMLabel,
            self.minDBLabel,
            self.minNMLabel,
            self.specificLabel,
            self.btnBaseline,
            self.btnSingle,
            self.btnContinuous,
            self.btnSaveData,
            self.btnSettings,
            self.btnWavelength,
        )
        self.progressBar.setProperty("value", 0)
        self.baseline.send_data("1")
        self.messageBox.setText("Measuring Baseline...")
        time.sleep(1)  # Esperar a que el arduino se inicialice

        self.timer.timeout.connect(self.baseline.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btn_status(self, status: bool):

        """Enable or disable buttons. If status is True, enable buttons. If status is False, disable buttons."""

        if status:
            self.btnBaseline.setEnabled(True)
            self.btnSingle.setEnabled(True)
            self.btnContinuous.setEnabled(True)
            self.btnSaveData.setEnabled(True)
            self.btnSettings.setEnabled(True)
            self.btnWavelength.setEnabled(True)
        else:
            self.btnBaseline.setDisabled(True)
            self.btnSingle.setDisabled(True)
            self.btnContinuous.setDisabled(True)
            self.btnSaveData.setDisabled(True)
            self.btnSettings.setDisabled(True)
            self.btnWavelength.setDisabled(True)

    def single(self):

        self.graphWidget.clear()
        self.single_process = SingleProcessor(
            self.graphWidget,
            self.pg,
            self.app,
            self.timer,
            self.progressBar,
            self.db450Label,
            self.db435Label,
            self.db500Label,
            self.db550Label,
            self.db570Label,
            self.db600Label,
            self.db650Label,
            self.maxDBLabel,
            self.maxNMLabel,
            self.minDBLabel,
            self.minNMLabel,
            self.specificLabel,
        )
        self.progressBar.setProperty("value", 0)

        self.single_process.send_data("2")
        self.messageBox.setText("Measuring Sample in single mode...")
        time.sleep(1)

        self.timer.timeout.connect(self.single_process.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btnSingle_click(self):
        print("Single Clicked")
        self.btn_status(False)
        self.single()
        


    def btnContinuous_click(self):
        print("Continuous Clicked")

        if not self.btn_continuous:
            self.btn_continuous = not self.btn_continuous
            self.btnContinuous.setText("Stop Continuous")

            self.btn_status(False)
            self.btnContinuous.setEnabled(True)

            self.single()

            if not self.timer_continue.isActive():
                self.timer_continue.start(5)

        else:

            self.btn_continuous = not self.btn_continuous
            self.btnContinuous.setText("Continuous")
            self.timer_continue.stop()
            self.btn_status(True)

    def timer_timeout(self):

        if self.timer.isActive():
            self.btn_status(False)
        else:
            self.btn_status(True)

        if self.btn_continuous and not self.timer.isActive():
            self.single()

    def btnSaveData_click(self):
        print("Save Data Clicked")
        self.messageBox.setText("Saving data...")
        self.saveDataWindow = SaveWindow(self)
        self.saveDataWindow.show()

    def btnSettings_click(self):
        print("Settings Clicked")
        self.messageBox.setText("Opening settings...")
        self.settingsWindow = SettingsWindow(self, self.backgroundColor)
        self.settingsWindow.saveSettingsRequested.connect(self.applySettings)
        self.settingsWindow.clearViewBoxRequested.connect(self.clearViewBox)
        self.settingsWindow.show()

        # Show the context menu of the ViewBox of the graph
        # self.graphWidget.getViewBox().menu.exec_()
        # self.graphWidget.getViewBox().autoRange()
        # self.graphWidget.getViewBox().setRange(xRange=(300, 500), yRange=(0, 1))
        # self.graphWidget.getViewBox().clear()
        # self.graphWidget.setLogMode(x=False, y=True)
        # self.graphWidget.setLogMode(x=True, y=False)
        # self.graphWidget.setDerivativeMode(True)
        # self.graphWidget.getViewBox().setBackgroundColor((255, 255, 255))

    def applySettings(self, settings):
        color, auto_range, x_range, y_range, log_mode_y, log_mode_x, derivative_mode = (
            settings
        )
        self.backgroundColor = color
        self.graphWidget.getViewBox().setBackgroundColor((color))
        if auto_range:
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.getViewBox().setRange(xRange=x_range, yRange=y_range)
        if log_mode_y:
            self.graphWidget.setLogMode(x=False, y=True)
        else:
            self.graphWidget.setLogMode(x=False, y=False)
        if log_mode_x:
            self.graphWidget.setLogMode(x=True, y=False)
        else:
            self.graphWidget.setLogMode(x=False, y=False)
        if derivative_mode:
            self.graphWidget.setDerivativeMode(True)
        else:
            self.graphWidget.setDerivativeMode(False)
        self.settingsWindow.close()

    def clearViewBox(self):
        self.graphWidget.getViewBox().clear()

    def btnWavelength_click(self):
        self.messageBox.setText("Selecting Wavelength...")
        nm, okPressed = QInputDialog.getInt(
            self, "Get dB", "Wavelength (nm):", 300, 300, 750, 1
        )
        if okPressed:
            line_value, message = get_line_value(nm)
            absorbance = get_absorbance(nm)
            print(line_value, message)
            QMessageBox.information(
                self, "Absorbance", f"{message}\nAbsorbance: {absorbance}"
            )

    def handleMainAction(self):
        print(f"Main action selected")

    def handleDataAction(self):
        print(f"Data action selected")
        with open("./data/wavelength_muestra.txt", "r") as f:
            wavelengths = [line.strip() for line in f]
        with open("./data/single_muestra.txt", "r") as f:
            absorbances = [line.strip() for line in f]

        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(400, 400)
        dialog.setWindowTitle("Data measured in single mode")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create a QTableWidget
        table = QtWidgets.QTableWidget(len(wavelengths), 2, dialog)
        table.setHorizontalHeaderLabels(["Wavelength", "Absorbance"])

        table.setColumnWidth(1, 200)  # Set the width of the "Absorbance" column to 200

        # Add the data to the table
        for i in range(len(wavelengths)):
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(wavelengths[i]))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(absorbances[i]))

        # Add the table to the layout
        layout.addWidget(table)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def handleSpanActionX(self):
        print(f"Span action selected")
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(100, 100)
        dialog.setWindowTitle("Select Range (X-axis)")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create a QLabel
        label = QtWidgets.QLabel(
            "Select the wavelength range you want to observe on the graph: "
        )
        layout.addWidget(label)

        # Create a QHBoxLayout for the start spin box and its label
        startLayout = QtWidgets.QHBoxLayout()
        startLabel = QtWidgets.QLabel("Start (nm):", dialog)
        start = QtWidgets.QSpinBox(dialog)
        start.setRange(300, 750)
        startLayout.addWidget(startLabel)
        startLayout.addWidget(start)

        # Add the start layout to the main layout
        layout.addLayout(startLayout)

        # Create a QHBoxLayout for the finish spin box and its label
        finishLayout = QtWidgets.QHBoxLayout()
        finishLabel = QtWidgets.QLabel("Finish (nm):", dialog)
        finish = QtWidgets.QSpinBox(dialog)
        finish.setRange(300, 750)
        finishLayout.addWidget(finishLabel)
        finishLayout.addWidget(finish)

        # Add the finish layout to the main layout
        layout.addLayout(finishLayout)

        # Create the "Apply" button
        applyButton = QtWidgets.QPushButton("Apply", dialog)
        applyButton.clicked.connect(
            lambda: self.applyRange(start.value(), finish.value())
        )
        layout.addWidget(applyButton)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def applyRange(self, start, finish):
        # Set the range of the x-axis of the graph
        self.graphWidget.setXRange(start, finish)


def init():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window(app=app)
    win.show()
    sys.exit(app.exec())

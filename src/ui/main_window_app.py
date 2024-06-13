import datetime
import math
import sys
import time
import qdarktheme
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QMainWindow,
    QMessageBox,
    QDesktopWidget,
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, QSpinBox
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
from pyqtgraph.exporters import CSVExporter
import PyQt5.QtGui as QtGui
from libs.wavelengths import wavelength
import numpy as np
import os


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.connectSignalsSlots()
        self.init()
        self.wavelengthFunction = wavelength()
        self.horaLabel.setText(datetime.datetime.now().strftime("%d-%m-%Y %H:%M"))
        self.showMaximized()

        # Create a QAction
        self.analysisAction = QtWidgets.QAction("Sample Integrity", self)
        # Add the QAction to the "Data" menu
        self.dataAnalysis.addAction(self.analysisAction)
        # Connect the QAction's triggered signal to a method
        self.analysisAction.triggered.connect(self.handleAnalysisAction)

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

        # Create a QAction
        self.spanActionY = QtWidgets.QAction("Select Range (Y-axis)", self)
        # Add the QAction to the "Data" menu
        self.spanData.addAction(self.spanActionY)
        # Connect the QAction's triggered signal to a method
        self.spanActionY.triggered.connect(self.handleSpanActionY)

        # Create a QAction
        self.graphType = QtWidgets.QAction("Select the graph type", self)
        # Add the QAction to the "Data" menu
        self.graphTypeAction.addAction(self.graphType)
        # Connect the QAction's triggered signal to a method
        self.graphType.triggered.connect(self.handleGraphType)

        # Create a QAction
        self.keyParameters = QtWidgets.QAction("Key Parameters", self)
        # Add the QAction to the "Data" menu
        self.parameters.addAction(self.keyParameters)
        # Connect the QAction's triggered signal to a method
        self.keyParameters.triggered.connect(self.handleKeyParameters)

        # Create a QAction
        self.radiometricParameters = QtWidgets.QAction("Radiometric Parameters", self)
        # Add the QAction to the "Data" menu
        self.parameters.addAction(self.radiometricParameters)
        # Connect the QAction's triggered signal to a method
        self.radiometricParameters.triggered.connect(self.handleRadiometricParameters)

        # Create a QAction
        self.electricalParameters = QtWidgets.QAction("Electrical Parameters", self)
        # Add the QAction to the "Data" menu
        self.parameters.addAction(self.electricalParameters)
        # Connect the QAction's triggered signal to a method
        self.electricalParameters.triggered.connect(self.handleElectricalParameters)

        # Create a QAction
        self.statisticalParameters = QtWidgets.QAction("Statistical Parameters", self)
        # Add the QAction to the "Data" menu
        self.parameters.addAction(self.statisticalParameters)
        # Connect the QAction's triggered signal to a method
        self.statisticalParameters.triggered.connect(self.handleStatisticalParameters)

        # Create a QAction
        self.aboutAction = QtWidgets.QAction("General Info", self)
        # Add the QAction to the "Data" menu
        self.about.addAction(self.aboutAction)
        # Connect the QAction's triggered signal to a method
        self.aboutAction.triggered.connect(self.handleAboutAction)

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
        self.graphWidget.getAxis('left').setLabel('Intensity')
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
            self.db440Label,
            self.db435Label,
            self.db465Label,
            self.db546Label,
            self.db590Label,
            self.db600Label,
            self.db635Label,
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
        self.graphWidget.setLabel("left", "Intensity")
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
            self.db440Label,
            self.db435Label,
            self.db465Label,
            self.db546Label,
            self.db590Label,
            self.db600Label,
            self.db635Label,
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
        self.graphWidget.setLabel("left", "Absorbance")
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
            self.db440Label,
            self.db435Label,
            self.db465Label,
            self.db546Label,
            self.db590Label,
            self.db600Label,
            self.db635Label,
            self.maxDBLabel,
            self.maxNMLabel,
            self.minDBLabel,
            self.minNMLabel,
            self.specificLabel,
        )
        self.progressBar.setProperty("value", 0)
        self.graphWidget.setLabel("left", "Absorbance")

        self.single_process.send_data("2")
        self.messageBox.setText("Measuring Sample in single mode...")
        time.sleep(1)

        self.timer.timeout.connect(self.single_process.process)
        self.timer.start(5)  # Actualiza cada 100 ms
        self.btn_status(True)

    def btnSingle_click(self):
        print("Single Clicked")
        self.btn_status(False)
        self.single()
        

    def btnContinuous_click(self):
        print("Continuous Clicked")
        self.graphWidget.setLabel("left", "Absorbance")

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

        # if self.timer.isActive():
        #     self.btn_status(False)
        # else:
        #     self.btn_status(True)

        if self.btn_continuous and not self.timer.isActive():
            self.single()

    def btnSaveData_click(self):
        print("Save Data Clicked")
        self.messageBox.setText("Saving data...")
        self.saveDataWindow = SaveWindow(self, graphWidget=self.graphWidget)

        # Set the window size
        self.saveDataWindow.resize(200, 300)  # Replace with the desired size

        qtRectangle = self.saveDataWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.saveDataWindow.move(qtRectangle.topLeft())

        self.saveDataWindow.show()

    def btnSettings_click(self):
        print("Settings Clicked")
        self.messageBox.setText("Opening settings...")
        self.settingsWindow = SettingsWindow(self, self.backgroundColor)
        self.settingsWindow.saveSettingsRequested.connect(self.applySettings)
        self.settingsWindow.clearViewBoxRequested.connect(self.clearViewBox)

        # Set the window size
        self.settingsWindow.resize(400, 300)  # Replace with the desired size

        qtRectangle = self.settingsWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.settingsWindow.move(qtRectangle.topLeft())


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
        color, auto_range, x_range, y_range, log_mode_y, log_mode_x, derivative_mode, invert_mode_y, invert_mode_x, antialiasing = (
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
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.setLogMode(x=False, y=False)
            self.graphWidget.getViewBox().autoRange()
        if log_mode_x:
            self.graphWidget.setLogMode(x=True, y=False)
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.setLogMode(x=False, y=False)
            self.graphWidget.getViewBox().autoRange()
        if derivative_mode:
            self.graphWidget.setDerivativeMode(True)
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.setDerivativeMode(False)
            self.graphWidget.getViewBox().autoRange()
        if invert_mode_y:
            self.graphWidget.getViewBox().invertY()
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.getViewBox().invertY(False)
            self.graphWidget.getViewBox().autoRange()
        if invert_mode_x:
            self.graphWidget.getViewBox().invertX()
            self.graphWidget.getViewBox().autoRange()
        else:
            self.graphWidget.getViewBox().invertX(False)
            self.graphWidget.getViewBox().autoRange()
        if antialiasing:
            #self.graphWidget.setRenderHints(QtGui.QPainter.Antialiasing)
            self.pg.setConfigOptions(antialias=True)
            #self.graphWidget.getViewBox().autoRange()
        else:
            self.pg.setConfigOptions(antialias=False)
            #self.graphWidget.getViewBox().autoRange()
        self.settingsWindow.close()

    def clearViewBox(self):
        self.graphWidget.getViewBox().clear()

    def btnWavelength_click(self):
        self.messageBox.setText("Selecting Wavelength...")

        # Create a custom dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("Get dB")
        layout = QVBoxLayout(dialog)

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        # Create the label and set its font
        text = QLabel("Wavelength (nm):")
        text.setFont(font)
        layout.addWidget(text)

        # Create the spin box and set its font
        nm_input = QSpinBox()
        nm_input.setRange(300, 750)
        nm_input.setValue(300)
        nm_input.setFont(font)
        layout.addWidget(nm_input)

        # Add OK and Cancel buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        # Set the font for each button
        for button in buttons.buttons():
            button.setStyleSheet("font-size: 14px;")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        # Show the dialog and get the result
        okPressed = dialog.exec_()
        nm = nm_input.value() if okPressed else None

        if nm is not None:
            absorbance = get_absorbance(nm)
            dialog = QDialog(self)
            dialog.setWindowTitle("Absorbance")
            layout = QVBoxLayout(dialog)

            # Create the label and set its font
            if absorbance is not None:
                text = QLabel(f"Wavelength: {nm}\nAbsorbance: {absorbance}")
            else:
                text = QLabel(f"No absorbance found for wavelength: {nm}")
            text.setFont(font)
            layout.addWidget(text)

            # Add OK button
            buttons = QDialogButtonBox(QDialogButtonBox.Ok)
            buttons.setFont(font)  # Set the font for the buttons
            buttons.accepted.connect(dialog.accept)
            layout.addWidget(buttons)

            dialog.exec_()

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
        table = QtWidgets.QTableWidget(445, 2, dialog)
        table.setHorizontalHeaderLabels(["Wavelength", "Absorbance"])

        table.setColumnWidth(1, 200)  # Set the width of the "Absorbance" column to 200

        # Assuming wavelengths and absorbances are lists
        wavelengths = np.array(wavelengths)
        absorbances = np.array(absorbances)

        # Create an array of new x values (i.e., 305, 306, 307, ...)
        new_wavelengths = np.arange(int(wavelengths[0]), int(wavelengths[-1]) + 1)

        # Interpolate the y values
        new_absorbances = np.interp((new_wavelengths.astype(float)), (wavelengths.astype(float)), (absorbances.astype(float)))

        # Now, new_wavelengths and new_absorbances are arrays that include the interpolated values.
        # You can use them to set the items in the table.

        for i in range(len(new_wavelengths)):
            table.setStyleSheet("""
                QScrollBar:vertical {
                    width: 30px;
                }
                QScrollBar:horizontal {
                    height: 30px;
                }
            """)
            table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(new_wavelengths[i])))
            table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(new_absorbances[i])))

        
        # Add the table to the layout
        layout.addWidget(table)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()
    
    def handleAnalysisAction(self):
        print(f"Analysis action selected")

        db440 = 40  # replace with the line number you want to read
        db450 = 66
        db465 = 91
        db480 = 114
        db500 = 124
        db525 = 148
        db546 = 66
        db565 = 91
        db580 = 114
        db590 = 124

        n440 = 40  # replace with the line number you want to read
        n450 = 66
        n465 = 91
        n480 = 114
        n500 = 124
        n525 = 148
        n546 = 66
        n565 = 91
        n580 = 114
        n590 = 124

        # 50 for 474, 56 for 428, 76 for 535, 97 for 587, 106 for 609, 120 for 600, 143 for 660
        with open("./data/single_muestra.txt", "r") as file:
            lines = file.readlines()
            if n440 <= len(lines):
                db440 = lines[n440 - 1].strip()
            if n450 <= len(lines):
                db450 = lines[n450 - 1].strip()
            if n465 <= len(lines):
                db465 = lines[n465 - 1].strip()
            if n480 <= len(lines):
                db480 = lines[n480 - 1].strip()
            if n500 <= len(lines):
                db500 = lines[n500 - 1].strip()
            if n525 <= len(lines):
                db525 = lines[n525 - 1].strip()
            if n546 <= len(lines):
                db546 = lines[n546 - 1].strip()
            if n565 <= len(lines):
                db565 = lines[n565 - 1].strip()
            if n580 <= len(lines):
                db580 = lines[n580 - 1].strip()
            if n590 <= len(lines):
                db590 = lines[n590 - 1].strip()
            else:
                print(f"The file has fewer than {n440} lines.")

        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(400, 450)
        dialog.setWindowTitle("Sample Integrity")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        if 0.4036 < float(db440) < 0.4796 and 0.0995 < float(db450) < 0.1755 and 0.2937 < float(db465) < 0.3697 and 0.2536 < float(db480) < 0.3296 and 0.1525 < float(db500) < 0.2285 and 0.01072 < float(db525) < 0.1832 and 0.1343 < float(db546) < 0.2103 and 0.1870 < float(db565) < 0.2630 and 0.1512 < float(db580) < 0.2272 and 0.1047 < float(db590) < 0.1807:
            # Create a QLabel
            label = QtWidgets.QLabel(
                "No contamination detected in the sample."
            )
            label.setFont(font)  # Set the font for the label
            label.setStyleSheet("color: green")
            layout.addWidget(label)
            if 0.4036 < float(db440) < 0.4796:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">440 nm: {float(db440):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">440 nm: {float(db440):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.0995 < float(db450) < 0.1755:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">450 nm: {float(db450):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">450 nm: {float(db450):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.2937 < float(db465) < 0.3697:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">465 nm: {float(db465):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">465 nm: {float(db465):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.2536 < float(db480) < 0.3296:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">480 nm: {float(db480):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">480 nm: {float(db480):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1525 < float(db500) < 0.2285:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">500 nm: {float(db500):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">500 nm: {float(db500):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.01072 < float(db525) < 0.1832:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">525 nm: {float(db525):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">525 nm: {float(db525):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1343 < float(db546) < 0.2103:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">546 nm: {float(db546):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">546 nm: {float(db546):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1870 < float(db565) < 0.2630:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">565 nm: {float(db565):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">565 nm: {float(db565):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1512 < float(db580) < 0.2272:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">580 nm: {float(db580):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">580 nm: {float(db580):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1047 < float(db590) < 0.1807:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">590 nm: {float(db590):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">590 nm: {float(db590):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
        else:
            # Create a QLabel
            label = QtWidgets.QLabel(
                "Contamination detected in the sample."
            )
            label.setFont(font)  # Set the font for the label
            label.setStyleSheet("color: red")
            layout.addWidget(label)
            if 0.4036 < float(db440) < 0.4796:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">440 nm: {float(db440):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">440 nm: {float(db440):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.0995 < float(db450) < 0.1755:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">450 nm: {float(db450):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">450 nm: {float(db450):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.2937 < float(db465) < 0.3697:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">465 nm: {float(db465):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">465 nm: {float(db465):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.2536 < float(db480) < 0.3296:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">480 nm: {float(db480):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">480 nm: {float(db480):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1525 < float(db500) < 0.2285:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">500 nm: {float(db500):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">500 nm: {float(db500):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.01072 < float(db525) < 0.1832:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">525 nm: {float(db525):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">525 nm: {float(db525):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1343 < float(db546) < 0.2103:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">546 nm: {float(db546):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">546 nm: {float(db546):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1870 < float(db565) < 0.2630:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">565 nm: {float(db565):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">565 nm: {float(db565):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1512 < float(db580) < 0.2272:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">580 nm: {float(db580):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">580 nm: {float(db580):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            if 0.1047 < float(db590) < 0.1807:
                label = QtWidgets.QLabel(f'<font color="green" size="5">■</font> <font color="white">590 nm: {float(db590):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)
            else:
                label = QtWidgets.QLabel(f'<font color="red" size="5">■</font> <font color="white">590 nm: {float(db590):.4f}</font>')
                label.setFont(font)
                layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

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

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        # Create a QLabel
        label = QtWidgets.QLabel(
            "Select the wavelength range you want to observe on the graph: "
        )
        label.setFont(font)  # Set the font for the label
        layout.addWidget(label)

        # Create a QHBoxLayout for the start spin box and its label
        startLayout = QtWidgets.QHBoxLayout()
        startLabel = QtWidgets.QLabel("Start (nm):", dialog)
        startLabel.setFont(font)  # Set the font for the start label
        start = QtWidgets.QSpinBox(dialog)
        start.setFont(font)  # Set the font for the start spin box
        start.setRange(300, 750)
        startLayout.addWidget(startLabel)
        startLayout.addWidget(start)

        # Add the start layout to the main layout
        layout.addLayout(startLayout)

        # Create a QHBoxLayout for the finish spin box and its label
        finishLayout = QtWidgets.QHBoxLayout()
        finishLabel = QtWidgets.QLabel("Finish (nm):", dialog)
        finishLabel.setFont(font)  # Set the font for the finish label
        finish = QtWidgets.QSpinBox(dialog)
        finish.setFont(font)  # Set the font for the finish spin box
        finish.setRange(300, 750)
        finishLayout.addWidget(finishLabel)
        finishLayout.addWidget(finish)

        # Add the finish layout to the main layout
        layout.addLayout(finishLayout)

        # Create the "Apply" button
        applyButton = QtWidgets.QPushButton("Apply", dialog)
        applyButton.setFont(font)  # Set the font for the apply button
        applyButton.clicked.connect(
            lambda: self.applyRange(start.value(), finish.value())
        )
        layout.addWidget(applyButton)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def applyRange(self, start, finish):
        # Set the range of the x-axis of the graph
        self.graphWidget.setXRange(start, finish)

    def handleSpanActionY(self):
        print(f"Span action selected")
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(100, 100)
        dialog.setWindowTitle("Select Range (Y-axis)")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        # Create a QLabel
        label = QtWidgets.QLabel(
            "Select the wavelength range you want to observe on the graph: "
        )
        label.setFont(font)  # Set the font for the label
        layout.addWidget(label)

        # Create a QHBoxLayout for the start spin box and its label
        startLayout = QtWidgets.QHBoxLayout()
        startLabel = QtWidgets.QLabel("Start (dB):", dialog)
        startLabel.setFont(font)  # Set the font for the start label
        start = QtWidgets.QSpinBox(dialog)
        start.setFont(font)  # Set the font for the start spin box
        start.setRange(-1, 10)
        startLayout.addWidget(startLabel)
        startLayout.addWidget(start)

        # Add the start layout to the main layout
        layout.addLayout(startLayout)

        # Create a QHBoxLayout for the finish spin box and its label
        finishLayout = QtWidgets.QHBoxLayout()
        finishLabel = QtWidgets.QLabel("Finish (dB):", dialog)
        finishLabel.setFont(font)  # Set the font for the finish label
        finish = QtWidgets.QSpinBox(dialog)
        finish.setFont(font)  # Set the font for the finish spin box
        finish.setRange(-1, 10)
        finishLayout.addWidget(finishLabel)
        finishLayout.addWidget(finish)

        # Add the finish layout to the main layout
        layout.addLayout(finishLayout)

        # Create the "Apply" button
        applyButton = QtWidgets.QPushButton("Apply", dialog)
        applyButton.setFont(font)  # Set the font for the apply button
        applyButton.clicked.connect(
            lambda: self.applyRangeY(start.value(), finish.value())
        )
        layout.addWidget(applyButton)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def applyRangeY(self, start, finish):
        # Set the range of the x-axis of the graph
        self.graphWidget.setYRange(start, finish)

    def handleGraphType(self):
        print(f"Span action selected")
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(100, 100)
        dialog.setWindowTitle("Select Graph Type")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()

        # Create a font
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        # Create a QLabel
        label = QtWidgets.QLabel(
            "Select the type of graph you want to use: "
        )
        label.setFont(font)  # Set the font for the label
        layout.addWidget(label)

        line = QtWidgets.QRadioButton("Line Graph (Default)", dialog)
        line.setFont(font)  # Set the font for the radio button
        line.setChecked(True)
        layout.addWidget(line)

        gaussian = QtWidgets.QRadioButton("Gaussian", dialog)
        gaussian.setFont(font)  # Set the font for the radio button
        layout.addWidget(gaussian)

        lorentzian = QtWidgets.QRadioButton("Lorentzian", dialog)
        lorentzian.setFont(font)  # Set the font for the radio button
        layout.addWidget(lorentzian)

        first_order = QtWidgets.QRadioButton("First Order", dialog)
        first_order.setFont(font)  # Set the font for the radio button
        layout.addWidget(first_order)

        second_order = QtWidgets.QRadioButton("Second Order", dialog)
        second_order.setFont(font)  # Set the font for the radio button
        layout.addWidget(second_order)

        third_order = QtWidgets.QRadioButton("Third Order", dialog)
        third_order.setFont(font)  # Set the font for the radio button
        layout.addWidget(third_order)

        fourth_order = QtWidgets.QRadioButton("Fourth Order", dialog)
        fourth_order.setFont(font)  # Set the font for the radio button
        layout.addWidget(fourth_order)

        # Create the "Apply" button
        applyButton = QtWidgets.QPushButton("Apply", dialog)
        applyButton.setFont(font)  # Set the font for the apply button
        layout.addWidget(applyButton)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def handleKeyParameters(self):
        print(f"Key Parameters action selected")

        db428 = 47  # replace with the line number you want to read
        db474 = 66
        db535 = 91
        db587 = 114
        db609 = 124
        db660 = 148

        n428 = 47  # replace with the line number you want to read
        n474 = 66
        n535 = 91
        n587 = 114
        n609 = 124
        n660 = 148
        # 50 for 474, 56 for 428, 76 for 535, 97 for 587, 106 for 609, 120 for 600, 143 for 660
        with open("./data/single_muestra.txt", "r") as file:
            lines = file.readlines()
            if n428 <= len(lines):
                db428 = lines[n428 - 1].strip()
            if n474 <= len(lines):
                db474 = lines[n474 - 1].strip()
            if n535 <= len(lines):
                db535 = lines[n535 - 1].strip()
            if n587 <= len(lines):
                db587 = lines[n587 - 1].strip()
            if n609 <= len(lines):
                db609 = lines[n609 - 1].strip()
            if n660 <= len(lines):
                db660 = lines[n660 - 1].strip()
            else:
                print(f"The file has fewer than {n428} lines.")

            maxDBvalue = float("-inf")
            maxnvalue = 0
            for i, line in enumerate(
                lines, start=1
            ):  # use lines instead of file
                value = float(line.strip())
                if value > maxDBvalue:
                    maxDBvalue = float(value)
                    # print(maxDBvalue)
                    maxnvalue = i
            maxNMvalue = int(
                self.wavelengthFunction[maxnvalue - 1]
            )  # get the corresponding nm value

            minDBvalue = float("inf")
            minNMvalue = 0
            for i, line in enumerate(lines, start=1):
                value = float(line.strip())
                if value < minDBvalue:
                    minDBvalue = float(value)
                    # print(minDBvalue)
                    minNMvalue = i
            minNMvalue = int(self.wavelengthFunction[minNMvalue - 1])

        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(300, 300)  # Increase the size to fit the information
        dialog.setWindowTitle("Key Parameters")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        #
        
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        label = QtWidgets.QLabel(
            "<b>Max dB: </b>" + str(maxDBvalue) + "<br><br>"
            "<b>Max nm: </b>" + str(maxNMvalue) + "<br><br>"
            "<b>Min dB: </b>" + str(minDBvalue) + "<br><br>"
            "<b>Min nm: </b>" + str(minNMvalue) + "<br><br>"
            "<b>Violet's (428nm): </b>" + str(db428) + "<br><br>"
            "<b>Blue's (474nm): </b>" + str(db474) + "<br><br>"
            "<b>Green's (535nm): </b>" + str(db535) + "<br><br>"
            "<b>Yellow's (587nm): </b>" + str(db587) + "<br><br>"
            "<b>Orange's (609nm): </b>" + str(db609) + "<br><br>"
            "<b>Red's (660nm): </b>" + str(db660) + "<br>"
        )
        label.setFont(font)
        layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()
    
    def handleRadiometricParameters(self):
        print(f"Radiometric Parameters action selected")
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(300, 300)  # Increase the size to fit the information
        dialog.setWindowTitle("Radiometric Parameters")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        #

        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        label = QtWidgets.QLabel(
            "<b>Radiant Flux:</b> 1000 rad<br><br>"
            "<b>Radiant Density:</b> 518 rad/mm2<br><br>"
            "<b>Color Rendering:</b> 70<br><br>"
            "<b>Thermal Resistance:</b> 1.6C°/W<br><br>"
            "<b>Radiant Efficacy:</b> 206 rad/W<br>"
        )
        label.setFont(font)
        layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)  # Set the font for the exit button
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()
    
    def handleElectricalParameters(self):
        print(f"Electrical Parameters action selected")
        # Create a QDialog
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(300, 300)  # Increase the size to fit the information
        dialog.setWindowTitle("Electrical Parameters")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        #
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        label = QtWidgets.QLabel(
            "<b>Voltage:</b> 12V<br><br>"
            "<b>Current:</b> 3A<br><br>"
            "<b>Power:</b> 36W<br><br>"
            "<b>Power Factor:</b> 1.0<br><br>"
            "<b>Frequency:</b> 60Hz<br>"
        )
        label.setFont(font)
        layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()
    
    def handleStatisticalParameters(self):
        print(f"Statistical Parameters action selected")
        with open("./data/single_muestra.txt", "r") as file:
            lines = file.readlines()
            mean = sum([float(line.strip()) for line in lines]) / len(lines)
            variance = sum([(float(line.strip()) - mean) ** 2 for line in lines]) / len(lines)
            standard_deviation = math.sqrt(variance)
            RMS = math.sqrt(sum([float(line.strip()) ** 2 for line in lines]) / len(lines))

            with open("./data/wavelength_muestra.txt", "r") as f:
                wavelengths = [line.strip() for line in f]
            with open("./data/single_muestra.txt", "r") as f:
                absorbances = [line.strip() for line in f]
            weighted_average = sum([float(wavelength) * float(absorbance) for wavelength, absorbance in zip(wavelengths, absorbances)]) / sum([float(absorbance) for absorbance in absorbances])

            maxDBvalue = float("-inf")
            maxnvalue = 0
            for i, line in enumerate(
                lines, start=1
            ):  # use lines instead of file
                value = float(line.strip())
                if value > maxDBvalue:
                    maxDBvalue = float(value)
                    # print(maxDBvalue)
                    maxnvalue = i
            maxNMvalue = int(
                self.wavelengthFunction[maxnvalue - 1]
            )  # get the corresponding nm value

            minDBvalue = float("inf")
            minNMvalue = 0
            for i, line in enumerate(lines, start=1):
                value = float(line.strip())
                if value < minDBvalue:
                    minDBvalue = float(value)
                    # print(minDBvalue)
                    minNMvalue = i
            minNMvalue = int(self.wavelengthFunction[minNMvalue - 1])

        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(300, 300)  # Increase the size to fit the information
        dialog.setWindowTitle("Statistical Parameters")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        #
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        label = QtWidgets.QLabel(
            "<b>Mean: </b>" + str(mean) + "<br><br>"
            "<b>Variance: </b>" + str(variance) + "<br><br>"
            "<b>Standard Deviation: </b>" + str(standard_deviation) + "<br><br>"
            "<b>RMS: </b>" + str(RMS) + "<br><br>"
            "<b>Weighted Average: </b>" + str(weighted_average) + "<br><br>"
            "<b>Max Value: </b>" + str(maxDBvalue) + "<br><br>"
            "<b>Min Value: </b>" + str(minDBvalue) + "<br><br>"
            "<b>Munmber of values: 198<br>"
        )
        label.setFont(font)
        layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()

    def handleAboutAction(self):
        print(f"About action selected")
        # Create a QDialog
        dialog = QtWidgets.QDialog(self)
        dialog.resize(300, 300)  # Increase the size to fit the information
        dialog.setWindowTitle("General Info")

        # Create a QVBoxLayout
        layout = QtWidgets.QVBoxLayout()
        #
        font = QtGui.QFont()
        font.setPointSize(14)  # Set the font size to 14 points

        label = QtWidgets.QLabel(
            "<b>Manufacturer:</b> UTP<br><br>"
            "<b>Laboratory:</b> Indicasat AIP<br><br>"
            "<b>Model:</b> UTP-CG-001<br><br>"
            "<b>Location:</b> Panama City, Panama<br><br>"
            "<b>Serial Number:</b> UTP30032024A<br><br>"
            "<b>Light Source:</b> High Power LED<br><br>"
            "<b>Wavelength Range:</b> 340 - 850 nm<br><br>"
            "<b>Detector:</b> CMOS<br><br>"
            "<b>Baseline Correction:</b> Yes<br><br>"
            "<b>Date:</b> " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "<br>"
        )
        label.setFont(font)
        layout.addWidget(label)

        # Create the "Exit" button
        exitButton = QtWidgets.QPushButton("Exit", dialog)
        exitButton.setFont(font)
        exitButton.clicked.connect(dialog.close)
        layout.addWidget(exitButton)

        # Set the layout of the dialog
        dialog.setLayout(layout)

        # Show the dialog
        dialog.exec_()
    

def init():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window(app=app)
    win.show()
    sys.exit(app.exec())

import sys
import time
import qdarktheme
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QMainWindow,
    QMessageBox,
    QGraphicsPixmapItem,
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

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, app=None):
        super().__init__(parent)
        self.app = app
        self.setupUi(self)
        self.connectSignalsSlots()
        self.init()
        

    def connectSignalsSlots(self):
        self.btnBaseline.clicked.connect(self.btnBaseline_click)
        self.btnSingle.clicked.connect(self.btnSingle_click)
        self.btnContinuous.clicked.connect(self.btnContinuous_click)
        self.btnSaveData.clicked.connect(self.btnSaveData_click)
        self.btnSettings.clicked.connect(self.btnSettings_click)
        self.btnWavelength.clicked.connect(self.btnWavelength_click)

        # self.btnBaseline.clicked.connect(self.btn_baseline)
        # self.btnSingle.clicked.connect(self.btn_single)
        # self.btnContinuous.clicked.connect(self.btn_continuous)
        # self.btnSaveData.clicked.connect(self.btn_save_data)
        # self.btnSettings.clicked.connect(self.btn_settings)

    def init(self):
        self.scene = QGraphicsScene()
        # self.graphicsView.setScene(self.scene)
        # pixmap = QPixmap("fie.jpg")
        # if not pixmap.isNull():
        #     image_item = QGraphicsPixmapItem(pixmap)
        #     self.scene.addItem(image_item)
        self.pg = pg
        self.timer = pg.QtCore.QTimer()
        

    def btnBaseline_click(self):
        print("Baseline Clicked")
        self.graphWidget.clear()
        self.baseline = BaselineProcessor(self.graphWidget, self.pg, self.app, self.timer, self.progressBar, self.db450Label, self.db435Label, self.db500Label, self.db550Label, self.db570Label, self.db600Label, self.db650Label, self.maxDBLabel, self.maxNMLabel, self.minDBLabel, self.minNMLabel, self.specificLabel)
        self.progressBar.setProperty("value", 0)
        self.baseline.send_data("1")
        self.messageBox.setText("Measuring Baseline...")
        time.sleep(1) # Esperar a que el arduino se inicialice

        self.timer.timeout.connect(self.baseline.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btnSingle_click(self):
        print("Single Clicked")
        self.graphWidget.clear()
        self.single = SingleProcessor(self.graphWidget, self.pg, self.app, self.timer, self.progressBar, self.db450Label, self.db435Label, self.db500Label, self.db550Label, self.db570Label, self.db600Label, self.db650Label, self.maxDBLabel, self.maxNMLabel, self.minDBLabel, self.minNMLabel, self.specificLabel)
        self.progressBar.setProperty("value", 0)

        # Sí el serial está activo, cerrar y abrir otro serial
        # if self.serial.is_open:
        #     self.serial.close()
        #     self.serial = Serial(PORT, BAUDRATE)

        self.single.send_data("2")
        self.messageBox.setText("Measuring Sample in single mode...")
        time.sleep(1)

        self.timer.timeout.connect(self.single.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btnContinuous_click(self):
        print("Continuous Clicked")
        self.graphWidget.clear()
        self.progressBar.setProperty("value", 0)
        self.messageBox.setText("Measuring Sample in continuous mode...")

    def btnSaveData_click(self):
        print("Save Data Clicked")
        self.messageBox.setText("Saving data...")
        self.saveDataWindow = SaveWindow(self)
        self.saveDataWindow.show()

    def btnSettings_click(self):
        print("Settings Clicked")
        self.messageBox.setText("Opening settings...")
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.show()

    def btnWavelength_click(self):
        self.messageBox.setText("Selecting Wavelength...")
        nm, okPressed = QInputDialog.getInt(self, "Get dB","Wavelength:", 0, 0, 10000, 1)
        if okPressed:
            line_value, message = get_line_value(nm)
            absorbance = get_absorbance(nm)
            print(line_value, message)
            QMessageBox.information(self, "Line Value", f"{message}\nAbsorbance: {absorbance}")



def init():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window(app=app)
    win.show()
    sys.exit(app.exec())

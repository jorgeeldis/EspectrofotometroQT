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

from ui.main_window_ui import Ui_MainWindow
import pyqtgraph as pg

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
        self.baseline = BaselineProcessor(self.graphWidget, self.pg, self.app, self.timer)

        self.baseline.send_data("1")
        time.sleep(1) # Esperar a que el arduino se inicialice

        self.timer.timeout.connect(self.baseline.process)
        self.timer.start(5)  # Actualiza cada 100 ms
        


    def prnt(self):
        print("Clock")

    def btnSingle_click(self):
        print("Single Clicked")
        self.graphWidget.clear()
        self.single = SingleProcessor(self.graphWidget, self.pg, self.app, self.timer)

        # Sí el serial está activo, cerrar y abrir otro serial
        # if self.serial.is_open:
        #     self.serial.close()
        #     self.serial = Serial(PORT, BAUDRATE)

        self.single.send_data("2")
        time.sleep(1)

        self.timer.timeout.connect(self.single.process)
        self.timer.start(5)  # Actualiza cada 100 ms

    def btn2_click(self):
        QMessageBox.about(
            self,
            "About Sample Editor",
            "<p>A sample text editor app built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )

    def btn_baseline(self):
        pass
    
    def btn_single(self):
        pass
    
    def btn_continuous(self):
        pass
    
    def btn_save_data(self):
        pass
    
    def btn_settings(self):
        pass


def init():
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    win = Window(app=app)
    win.show()
    sys.exit(app.exec())

import sys
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
        print("CLICKED - BaseLine")
        self.graphWidget.clear()
        self.baseline = BaselineProcessor(self.graphWidget, self.pg, self.app, self.timer)
        self.timer.timeout.connect(self.baseline.process)
        self.timer.start(5)  # Actualiza cada 100 ms
        


    def prnt(self):
        print("Clock")

    def btnSingle_click(self):
        print("CLICKED - 1")

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
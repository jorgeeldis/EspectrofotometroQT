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

from ui.main_window_ui import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()
        self.init()

    def connectSignalsSlots(self):
        self.pushButton_2.clicked.connect(self.btn2_click)
        self.pushButton.clicked.connect(self.btn1_click)

        # self.btnBaseline.clicked.connect(self.btn_baseline)
        # self.btnSingle.clicked.connect(self.btn_single)
        # self.btnContinuous.clicked.connect(self.btn_continuous)
        # self.btnSaveData.clicked.connect(self.btn_save_data)
        # self.btnSettings.clicked.connect(self.btn_settings)

    def init(self):
        self.scene = QGraphicsScene()
        self.graphicsView_2.setScene(self.scene)
        pixmap = QPixmap("fie.jpg")
        if not pixmap.isNull():
            image_item = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(image_item)

    def btn1_click(self):
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
    win = Window()
    win.show()
    sys.exit(app.exec())

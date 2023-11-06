import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QMenu, QAction, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle("Ventana con PyQt5 y pyqtgraph")
        self.setGeometry(100, 100, 800, 600)

        # Menú en la parte superior
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Archivo")
        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Contenedor central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Gráfica con pyqtgraph en el centro
        self.plot_widget = pg.PlotWidget(title="Gráfica")
        layout.addWidget(self.plot_widget)

        # Imágenes a la derecha de la gráfica
        image1 = QLabel()
        pixmap1 = QPixmap("fie.jpg")  # Ruta de la primera imagen
        image1.setPixmap(pixmap1)
        layout.addWidget(image1)

        image2 = QLabel()
        pixmap2 = QPixmap("fie.jpg")  # Ruta de la segunda imagen
        image2.setPixmap(pixmap2)
        layout.addWidget(image2)

        # Botones debajo de la gráfica
        button1 = QPushButton("Botón 1")
        layout.addWidget(button1)

        button2 = QPushButton("Botón 2")
        layout.addWidget(button2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

import sys
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenuBar, QAction, QVBoxLayout, QWidget, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Ventana con pyqtgraph")

        # Crear un menú
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Archivo')
        exit_action = QAction('Salir', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Crear el widget principal que contendrá todo
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Crear una disposición horizontal para organizar los elementos
        layout = QHBoxLayout(main_widget)

        # Crear la gráfica con pyqtgraph
        plot_widget = pg.PlotWidget()
        layout.addWidget(plot_widget)

        # Crear una disposición vertical para las imágenes y los botones
        right_layout = QVBoxLayout()

        # Crear dos etiquetas de imagen
        image_label1 = QLabel()
        image_label2 = QLabel()

        # Configurar las imágenes en las etiquetas (reemplaza 'imagen1.png' y 'imagen2.png' con las rutas de tus imágenes)
        image1_pixmap = QPixmap('fie.jpg')
        image2_pixmap = QPixmap('fie.jpg')
        image_label1.setPixmap(image1_pixmap)
        image_label2.setPixmap(image2_pixmap)

        right_layout.addWidget(image_label1)
        right_layout.addWidget(image_label2)

        # Crear dos botones
        button1 = QPushButton("Botón 1")
        button2 = QPushButton("Botón 2")
        right_layout.addWidget(button1)
        right_layout.addWidget(button2)

        # Agregar la disposición de la derecha al diseño principal
        layout.addLayout(right_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

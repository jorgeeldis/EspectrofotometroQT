import sys
import serial
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

import pyqtgraph as pg
from wavelengths import wavelength
from absorption_calc import absorption

# Crear una aplicación Qt
app = QApplication(sys.argv)

# Crear una ventana principal
window = QMainWindow()
window.setWindowTitle("Gráfica en tiempo real desde Arduino")

# btn_1 = QPushButton("Botón 1")
# btn_2 = QPushButton("Botón 2")
# btn_1.setGeometry(10, 10, 100, 30)
# btn_2.setGeometry(120, 10, 100, 30)


# Crear un widget para la gráfica
graphWidget = pg.PlotWidget()
graphWidget.setXRange(420, 750, padding=0)
# graphWidget.setYRange(-0.1, 2.1, padding=0)
graphWidget.setAutoFillBackground(True)
graphWidget.setBackgroundBrush(QtCore.Qt.white)
graphWidget.showGrid(x=True, y=True, alpha=0.3)
brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
brush.setStyle(QtCore.Qt.NoBrush)
graphWidget.setForegroundBrush(brush)

window.setCentralWidget(graphWidget)


window.show()

# Configurar el puerto serie para comunicarse con el Arduino (ajusta el puerto y la velocidad en baudios según tu configuración) #/dev/ttyACM0 #COM3
ser = serial.Serial("/dev/ttyACM0", 9600)


def read_baselines():
    BASELINE = "baseline_muestra.txt"
    """Leer los datos del archivo de texto."""
    try:
        file = open(BASELINE, "r")
        data = file.read()
        file.close()
        return data
    except Exception as e:
        print(e)


# Inicializar la lista de datos y el eje x
ydata = []
xdata = []
x = 0
wavelength = wavelength()
base_line_values = read_baselines()
base_line_data = base_line_values.split("\n")


# Función para actualizar la gráfica en tiempo real
def update():
    global wavelength
    global x
    global ydata, xdata
    global base_line_data

    line = ser.readline().decode("utf-8")
    # print(len(line), line)

    if len(line) == 9:
        intensity = int(line.split(",")[1])

        baseline = base_line_data[x]
        # print(baseline, intensity)
        absorbance = absorption(int(baseline), int(intensity))

        xdata.append(int(wavelength[x]))
        ydata.append(absorbance)

        data_to_save = {
            "wavelength": wavelength[x],
            "absorbance": absorbance,
            "intensity": intensity,
        }
        print(data_to_save)

        if int(wavelength[x]) > 748:
            timer.stop()

        graphWidget.plot(xdata, ydata, pen=pg.mkPen("b", width=2))
        x += 1
        app.processEvents()


# Crear un temporizador para actualizar la gráfica cada cierto tiempo
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)  # Actualiza cada 100 ms

# Ejecutar la aplicación
if __name__ == "__main__":
    sys.exit(app.exec_())

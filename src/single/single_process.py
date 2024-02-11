import os
from pathlib import Path
import time
from dotenv import load_dotenv
from libs.absorption_calc import absorption
from libs.fileutil import read_data, write_data
from libs.serial_comunication import Serial
from libs.wavelengths import wavelength

load_dotenv()

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

DATA_SIZE = 7

BASELINE_FILE = os.getenv("BASELINE_FILE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)

class SingleProcessor:
    def __init__(self, graphWidget, pg, app, timer):

        self.single = 0
        self.file_name = "single_muestra_{}_{}.txt".format(
            self.single, time.strftime("%Y%m%d-%H%M%S")
        )
        # Baseline file
        self.baseline_path = baseline_path
        self.timer = timer
        self.app = app
        self.graphWidget = graphWidget
        self.pg = pg
        self.serial = Serial(PORT, BAUDRATE)
        self.wavelength = wavelength()

        self.ydata = []
        self.xdata = []
        self.x = 0
        self.baseline_x = 0

        # Leer el archivo de baseline
        read_baseline = read_data(self.baseline_path)
        self.baseline_data = read_baseline.split("\n")

    def clear_graph(self):
        self.graphWidget.clear()

    def process(self):
                
        # Lee datos desde el arduino
        data = self.serial.read()

        print(len(data), data)

        # Se asegura que el dato recibido tenga el tamaño correcto
        if len(data) == DATA_SIZE:
            
            # baseline data
            baseline = int(self.baseline_data[self.baseline_x])

            # intensidad
            intensity = int(data.split(",")[1])

            # Calcular la absorbancia
            absorbance = absorption(int(baseline), int(intensity))

            wavelength_data = int(self.wavelength[self.x])

            self.xdata.append(wavelength_data)
            self.ydata.append(absorbance)

            data_to_save = {
                "wavelength": wavelength_data,
                "absorbance": absorbance,
                "intensity": intensity,
            }
            print(data_to_save)

            if int(wavelength_data) > 748:
                self.ydata = []
                self.xdata = []
                self.x = 0
                self.baseline_x = 0
                self.timer.stop()
                self.serial.close()

            # Los grafica en tiempo real
            self.graphWidget.plot(self.xdata, self.ydata, pen=self.pg.mkPen("b", width=2))
            self.x += 1
            self.baseline_x += 1
            self.app.processEvents()
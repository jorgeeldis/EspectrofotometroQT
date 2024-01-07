import os
from pathlib import Path
from dotenv import load_dotenv
from libs.fileutil import write_data
from libs.serial_comunication import Serial
from libs.wavelengths import wavelength

load_dotenv()

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

BASELINE_FILE = os.getenv("BASELINE_FILE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)

class BaselineProcessor:
    def __init__(self, graphWidget, pg, app, timer):

        if os.path.exists(baseline_path):
            os.remove(baseline_path)

        self.timer = timer
        self.app = app
        self.graphWidget = graphWidget
        self.pg = pg
        self.serial = Serial(PORT, BAUDRATE)
        self.wavelength = wavelength()

        self.ydata = []
        self.xdata = []
        self.x = 0

    def process(self):
        # Lee datos desde el arduino
        data = self.serial.read()

        print(len(data), data)

        # Se asegura que el dato recibido tenga el tamaño correcto
        if len(data) == 7:
            # intensidad
            intensity = int(data.split(",")[1])
       
            # Guarda los datos en un archivo de texto
            write_data(baseline_path, str(intensity) + "\n")

            self.xdata.append(int(self.wavelength[self.x]))
            self.ydata.append(intensity)

            if int(self.wavelength[self.x]) > 748:
                self.ydata = []
                self.xdata = []
                self.x = 0
                self.timer.stop()
                self.serial.close()

            # Los grafica en tiempo real
            self.graphWidget.plot(self.xdata, self.ydata, pen=self.pg.mkPen("b", width=2))
            self.x += 1
            self.app.processEvents()
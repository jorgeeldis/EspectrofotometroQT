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
    def __init__(self, graphWidget, pg, app, timer, progressBar):

        if os.path.exists(baseline_path):
            os.remove(baseline_path)

        self.timer = timer
        self.app = app
        self.graphWidget = graphWidget
        self.progressBar = progressBar
        self.pg = pg
        self.serial = Serial(PORT, BAUDRATE)
        self.wavelength = wavelength()

        self.ydata = []
        self.xdata = []
        self.x = 0

    def process(self):

        # Lee datos desde el arduino
        data = self.serial.read()
        
        # Se asegura que el dato recibido tenga el tamaño correcto
        if data is not None and len(data) == 7:

            print(len(data), data)
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
            if self.progressBar.value() < 100:
                self.x += 1
                progresspercent = int(self.x / 196 * 100)
                self.progressBar.setValue(progresspercent)
                print(progresspercent)
            self.app.processEvents()
           

    def send_data(self, data):
        self.serial.write(str.encode(data))
import os
from pathlib import Path
import time
from dotenv import load_dotenv
from libs.absorption_calc import absorption
from libs.fileutil import read_data, write_data
from libs.interpolation import interpolate
from libs.serial_comunication import Serial
from libs.wavelengths import wavelength
from libs.log_util import config_logger

logger = config_logger()

load_dotenv()

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

value = os.getenv("DEBUG")
DEBUG = {"true": True, "false": False}.get(value.lower())

DATA_SIZE = 7

BASELINE_FILE = os.getenv("BASELINE_FILE")
SINGLE_FILE = os.getenv("SINGLE_FILE")
WAVELENGTH_FILE = os.getenv("WAVELENGTH_FILE")
INTERPOLATE_FILE = os.getenv("INTERPOLATE_FILE")

PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)
single_path = os.path.join("data", SINGLE_FILE)
wavelength_path = os.path.join("data", WAVELENGTH_FILE)
interpolate_path = os.path.join("data", INTERPOLATE_FILE)

class SingleProcessor:
    def __init__(
        self,
        graphWidget,
        pg,
        app,
        timer,
        progressBar,
        db435Label,
        db440Label,
        db465Label,
        db546Label,
        db590Label,
        db600Label,
        db635Label,
        maxDBLabel,
        maxNMLabel,
        minDBLabel,
        minNMLabel,
        specificLabel,
    ):

        if os.path.exists(single_path):
            os.remove(single_path)

        if os.path.exists(wavelength_path):
            os.remove(wavelength_path)

        self.single = 0
        self.file_name = "single_muestra_{}_{}.txt".format(
            self.single, time.strftime("%Y%m%d-%H%M%S")
        )
        # Baseline file
        self.baseline_path = baseline_path
        self.timer = timer
        self.app = app
        self.graphWidget = graphWidget

        self.progressBar = progressBar
        self.db435Label = db435Label
        self.db440Label = db440Label
        self.db465Label = db465Label
        self.db546Label = db546Label
        self.db590Label = db590Label
        self.db600Label = db600Label
        self.db635Label = db635Label
        self.maxDBLabel = maxDBLabel
        self.maxNMLabel = maxNMLabel
        self.minDBLabel = minDBLabel
        self.minNMLabel = minNMLabel

        self.specificLabel = specificLabel
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

        # Se asegura que el dato recibido tenga el tamaño correcto
        if data is not None and len(data) == DATA_SIZE:

            if DEBUG:
                data_log = "Data Length: {}, Data: {}".format(len(data), data)
                logger.debug(data_log)

            # baseline data
            baseline = int(self.baseline_data[self.baseline_x])

            # intensidad
            intensity = int(data.split(",")[1])

            # Calcular la absorbancia
            absorbance = absorption(int(baseline), int(intensity))

            # TODO: Guardar los datos de la absorbancia
            write_data(single_path, str(absorbance) + "\n")

            wavelength_data = int(self.wavelength[self.x])

            # TODO: Guardar los datos de la longitud de onda
            write_data(wavelength_path, str(wavelength_data) + "\n")

            self.xdata.append(wavelength_data)
            self.ydata.append(absorbance)

            data_to_save = {
                "wavelength": wavelength_data,
                "absorbance": absorbance,
                "intensity": intensity,
            }

            if DEBUG:
                logger.debug(data_to_save)

            if int(wavelength_data) > 748:
                self.ydata = []
                self.xdata = []
                self.x = 0
                self.baseline_x = 0
                self.timer.stop()
                self.serial.close()

            # Los grafica en tiempo real
            self.graphWidget.plot(
                self.xdata, self.ydata, pen=self.pg.mkPen("b", width=2)
            )
            self.x += 1
            self.baseline_x += 1

            if self.progressBar.value() < 100:

                progresspercent = int(self.x / 196 * 100)
                self.progressBar.setValue(progresspercent)

            if self.progressBar.value() == 100:
                wavelengths = [435, 440, 465, 546, 590, 600, 635]
                db_values = {wavelength: None for wavelength in wavelengths}

                with open("./data/interpolate_muestra.txt", "r") as file:
                    lines = file.readlines()
                    for line in lines:
                        wavelength, db = line.strip().split(',')
                        wavelength = int(wavelength)
                        db = float(db)
                        if wavelength in db_values:
                            db_values[wavelength] = db

                    db435 = db_values[435]
                    db440 = db_values[440]
                    db465 = db_values[465]
                    db546 = db_values[546]
                    db590 = db_values[590]
                    db600 = db_values[600]
                    db635 = db_values[635]

                    maxDBvalue = float("-inf")
                    maxNMvalue = None
                    for i, line in enumerate(lines, start=1):
                        wavelength, value = line.strip().split(',')
                        value = float(value)
                        if value > maxDBvalue:
                            maxDBvalue = value
                            maxNMvalue = int(wavelength)

                    minDBvalue = float("inf")
                    minNMvalue = None
                    for i, line in enumerate(lines, start=1):
                        wavelength, value = line.strip().split(',')
                        value = float(value)
                        if value < minDBvalue:
                            minDBvalue = value
                            minNMvalue = int(wavelength)

                # Garda archivo de interpolación
                interpolate()

                self.specificLabel.setText("Key Values:")
                self.db440Label.setText(
                    "440nm: " + str("{:.4f}".format(float(db440))) + "dB"
                )
                self.db435Label.setText(
                    "435nm: " + str("{:.4f}".format(float(db435))) + "dB"
                )
                self.db465Label.setText(
                    "465nm: " + str("{:.4f}".format(float(db465))) + "dB"
                )
                self.db546Label.setText(
                    "546nm: " + str("{:.4f}".format(float(db546))) + "dB"
                )
                self.db590Label.setText(
                    "590nm: " + str("{:.4f}".format(float(db590))) + "dB"
                )
                self.db600Label.setText(
                    "600nm: " + str("{:.4f}".format(float(db600))) + "dB"
                )
                self.db635Label.setText(
                    "635nm: " + str("{:.4f}".format(float(db635))) + "dB"
                )
                self.maxDBLabel.setText(
                    "Max dB: " + str("{:.4f}".format(float(maxDBvalue))) + "dB"
                )
                self.maxNMLabel.setText("Max nm: " + str(maxNMvalue) + "nm")
                self.minDBLabel.setText(
                    "Min dB: " + str("{:.4f}".format(float(minDBvalue))) + "dB"
                )
                self.minNMLabel.setText("Min nm: " + str(minNMvalue) + "nm")

            self.app.processEvents()

    def send_data(self, data):
        self.serial.write(str.encode(data))

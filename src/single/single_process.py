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
        db450Label,
        db435Label,
        db500Label,
        db550Label,
        db570Label,
        db600Label,
        db650Label,
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
        self.db450Label = db450Label
        self.db435Label = db435Label
        self.db500Label = db500Label 
        self.db550Label = db550Label
        self.db570Label = db570Label
        self.db600Label = db600Label
        self.db650Label = db650Label
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
                n450 = 56  # replace with the line number you want to read
                n435 = 50
                n500 = 76
                n550 = 97
                n570 = 106
                n600 = 120
                n650 = 143
                # 50 for 435, 56 for 450, 76 for 500, 97 for 550, 106 for 570, 120 for 600, 143 for 650
                with open("./data/single_muestra.txt", "r") as file:
                    lines = file.readlines()
                    if n450 <= len(lines):
                        db450 = lines[n450 - 1].strip()
                    if n435 <= len(lines):
                        db435 = lines[n435 - 1].strip()
                    if n500 <= len(lines):
                        db500 = lines[n500 - 1].strip()
                    if n550 <= len(lines):
                        db550 = lines[n550 - 1].strip()
                    if n570 <= len(lines):
                        db570 = lines[n570 - 1].strip()
                    if n600 <= len(lines):
                        db600 = lines[n600 - 1].strip()
                    if n650 <= len(lines):
                        db650 = lines[n650 - 1].strip()
                    else:
                        print(f"The file has fewer than {n450} lines.")

                    maxDBvalue = float("-inf")
                    maxnvalue = 0
                    for i, line in enumerate(
                        lines, start=1
                    ):  # use lines instead of file
                        value = float(line.strip())
                        if value > maxDBvalue:
                            maxDBvalue = float(value)
                            # print(maxDBvalue)
                            maxnvalue = i
                    maxNMvalue = int(
                        self.wavelength[maxnvalue - 1]
                    )  # get the corresponding nm value

                    minDBvalue = float("inf")
                    minNMvalue = 0
                    for i, line in enumerate(lines, start=1):
                        value = float(line.strip())
                        if value < minDBvalue:
                            minDBvalue = float(value)
                            # print(minDBvalue)
                            minNMvalue = i
                    minNMvalue = int(self.wavelength[minNMvalue - 1])

                # Garda archivo de interpolación
                interpolate()

                self.specificLabel.setText("Key Values (dB):")
                self.db450Label.setText(
                    "450nm: " + str("{:.2f}".format(float(db450))) + "dB"
                )
                self.db435Label.setText(
                    "435nm: " + str("{:.2f}".format(float(db435))) + "dB"
                )
                self.db500Label.setText(
                    "500nm: " + str("{:.2f}".format(float(db500))) + "dB"
                )
                self.db550Label.setText(
                    "550nm: " + str("{:.2f}".format(float(db550))) + "dB"
                )
                self.db570Label.setText(
                    "570nm: " + str("{:.2f}".format(float(db570))) + "dB"
                )
                self.db600Label.setText(
                    "600nm: " + str("{:.2f}".format(float(db600))) + "dB"
                )
                self.db650Label.setText(
                    "650nm: " + str("{:.2f}".format(float(db650))) + "dB"
                )
                self.maxDBLabel.setText(
                    "Max dB: " + str("{:.2f}".format(float(maxDBvalue))) + "dB"
                )
                self.maxNMLabel.setText("Max nm: " + str(maxNMvalue) + "nm")
                self.minDBLabel.setText(
                    "Min dB: " + str("{:.2f}".format(float(minDBvalue))) + "dB"
                )
                self.minNMLabel.setText("Min nm: " + str(minNMvalue) + "nm")

            self.app.processEvents()

    def send_data(self, data):
        self.serial.write(str.encode(data))

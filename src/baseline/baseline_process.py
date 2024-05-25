import os
from pathlib import Path
from dotenv import load_dotenv
from libs.fileutil import write_data
from libs.serial_comunication import Serial
from libs.wavelengths import wavelength
from libs.log_util import config_logger

logger = config_logger()

load_dotenv()

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

value = os.getenv("DEBUG")
DEBUG = {"true": True, "false": False}.get(value.lower())


BASELINE_FILE = os.getenv("BASELINE_FILE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)

class BaselineProcessor:
    def __init__(self, graphWidget, pg, app, timer, progressBar, db435Label,
        db440Label,
        db465Label,
        db546Label,
        db590Label,
        db600Label,
        db635Label, maxDBLabel, maxNMLabel, minDBLabel, minNMLabel, specificLabel, btnBaseline, btnSingle, btnContinuous, btnSaveData, btnSettings, btnWavelength):

        if os.path.exists(baseline_path):
            os.remove(baseline_path)

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
        self.btnBaseline = btnBaseline
        self.btnSingle = btnSingle
        self.btnContinuous = btnContinuous
        self.btnSaveData = btnSaveData
        self.btnSettings = btnSettings
        self.btnWavelength = btnWavelength
        self.specificLabel = specificLabel
        self.pg = pg
        self.serial = Serial(PORT, BAUDRATE)
        self.wavelength = wavelength()

        self.ydata = []
        self.xdata = []
        self.x = 0
        self.accum = 0

    def process(self):

        # Lee datos desde el arduino
        data = self.serial.read()
        
        # Se asegura que el dato recibido tenga el tamaño correcto
        if data is not None and len(data) == 7:

            self.accum += 1
            
            if DEBUG:
                data_log = "Data Length: {}, Data: {}, Acumulado: {}".format(len(data), data, self.accum)
                logger.debug(data_log)
            
            # intensidad
            intensity = int(data.split(",")[1])
       
            # Guarda los datos en un archivo de texto
            write_data(baseline_path, str(intensity) + "\n")

            wavelength = int(self.wavelength[self.x])
            if 311 <= wavelength <= 748:
                self.xdata.append(wavelength)
                self.ydata.append(intensity)

                # Los grafica en tiempo real
                self.graphWidget.plot(self.xdata, self.ydata, pen=self.pg.mkPen("b", width=2))

            if wavelength > 748:
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
                #print(progresspercent)
            if self.progressBar.value() == 100:
                n435 = 53
                n440 = 55
                n465 = 65
                n546 = 99
                n590 = 118
                n600 = 123
                n635 = 139
                # 50 for 435, 56 for 450, 76 for 500, 97 for 550, 106 for 570, 120 for 600, 143 for 650
                with open('./data/baseline_muestra.txt', 'r') as file:
                    lines = file.readlines()
                    if n440 <= len(lines):
                        db440 = lines[n440 - 1].strip()
                    if n435 <= len(lines):
                        db435 = lines[n435 - 1].strip()
                    if n465 <= len(lines):
                        db465 = lines[n465 - 1].strip()
                    if n546 <= len(lines):
                        db546 = lines[n546 - 1].strip()
                    if n590 <= len(lines):
                        db590 = lines[n590 - 1].strip()
                    if n600 <= len(lines):
                        db600 = lines[n600 - 1].strip()
                    if n635 <= len(lines):
                        db635 = lines[n635 - 1].strip()
                    else:
                        print(f"The file has fewer than {n440} lines.")

                    maxDBvalue = float('-inf')
                    maxnvalue = 0
                    for i, line in enumerate(lines, start=1):  # use lines instead of file
                        value = float(line.strip())
                        if value > maxDBvalue:
                            maxDBvalue = int(value)
                            maxnvalue = i
                    maxNMvalue = int(self.wavelength[maxnvalue - 1])  # get the corresponding nm value
                    
                    minDBvalue = float('inf')
                    minNMvalue = 0
                    for i, line in enumerate(lines, start=1):
                        value = float(line.strip())
                        if value < minDBvalue:
                            minDBvalue = int(value)
                            minNMvalue = i
                    minNMvalue = int(self.wavelength[minNMvalue - 1])

                self.specificLabel.setText("Key Values (u.a.):")
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
                self.maxDBLabel.setText("Max u.a.: " + str("{:.4f}".format(float(maxDBvalue))) + "u.a.")
                self.maxNMLabel.setText("Max nm: " + str(maxNMvalue) + "nm")
                self.minDBLabel.setText("Min u.a.: " + str("{:.4f}".format(float(minDBvalue))) + "u.a.")
                self.minNMLabel.setText("Min nm: " + str(minNMvalue) + "nm")
                # Enable buttons
                self.btnBaseline.setDisabled(False)
                self.btnSingle.setDisabled(False)
                self.btnContinuous.setDisabled(False)
                self.btnSaveData.setDisabled(False)
                self.btnSettings.setDisabled(False)
                self.btnWavelength.setDisabled(False)
            self.app.processEvents()
           

    def send_data(self, data):
        self.serial.write(str.encode(data))
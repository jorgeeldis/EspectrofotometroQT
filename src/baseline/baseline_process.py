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
    def __init__(self, graphWidget, pg, app, timer, progressBar, db450Label, db435Label, db500Label, db550Label, db570Label, db600Label, db650Label, maxDBLabel, maxNMLabel, minDBLabel, minNMLabel):

        if os.path.exists(baseline_path):
            os.remove(baseline_path)

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

            print(len(data), data)
            self.accum += 1
            print(self.accum)
            
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
                #print(progresspercent)
            if self.progressBar.value() == 100:
                n450 = 56  # replace with the line number you want to read
                n435 = 50
                n500 = 76
                n550 = 97
                n570 = 106
                n600 = 120
                n650 = 143
                # 50 for 435, 56 for 450, 76 for 500, 97 for 550, 106 for 570, 120 for 600, 143 for 650
                with open('./data/baseline_muestra.txt', 'r') as file:
                    lines = file.readlines()
                    if n450 <= len(lines):
                        db450 = lines[n450-1].strip()
                    if n435 <= len(lines):
                        db435 = lines[n435-1].strip()
                    if n500 <= len(lines):
                        db500 = lines[n500-1].strip()
                    if n550 <= len(lines):
                        db550 = lines[n550-1].strip()
                    if n570 <= len(lines):
                        db570 = lines[n570-1].strip()
                    if n600 <= len(lines):
                        db600 = lines[n600-1].strip()
                    if n650 <= len(lines):
                        db650 = lines[n650-1].strip()
                    else:
                        print(f"The file has fewer than {n450} lines.")

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

                self.db450Label.setText("dB 450nm: " + str(db450))
                self.db435Label.setText("dB 435nm: " + str(db435))
                self.db500Label.setText("dB 500nm: " + str(db500))
                self.db550Label.setText("dB 550nm: " + str(db550))
                self.db570Label.setText("dB 570nm: " + str(db570))
                self.db600Label.setText("dB 600nm: " + str(db600))
                self.db650Label.setText("dB 650nm: " + str(db650))
                self.maxDBLabel.setText("Max dB: " + str(maxDBvalue))
                self.maxNMLabel.setText("Max nm: " + str(maxNMvalue))
                self.minDBLabel.setText("Min dB: " + str(minDBvalue))
                self.minNMLabel.setText("Min nm: " + str(minNMvalue))
            self.app.processEvents()
           

    def send_data(self, data):
        self.serial.write(str.encode(data))
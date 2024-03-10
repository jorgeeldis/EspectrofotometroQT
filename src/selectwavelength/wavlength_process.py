import os
from pathlib import Path
import time
from dotenv import load_dotenv
from libs.absorption_calc import absorption
from libs.fileutil import read_data, write_data
from libs.serial_comunication import Serial
from libs.wavelengths import wavelength
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton


load_dotenv()

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

DATA_SIZE = 7

BASELINE_FILE = os.getenv("BASELINE_FILE")
SINGLE_FILE = os.getenv("SINGLE_FILE")
WAVELENGTH_FILE = os.getenv("WAVELENGTH_FILE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)
single_path = os.path.join("data", SINGLE_FILE)
wavelength_path = os.path.join("data", WAVELENGTH_FILE)

def get_line_value(nm):
    with open(wavelength_path, 'r') as file:
        lines = [float(line.strip()) for line in file.readlines()]
        # Find the line with the value closest to nm
        closest_line_wavelength = min(range(len(lines)), key=lambda index: abs(lines[index]-nm))
        closest_value_wavelength = lines[closest_line_wavelength]
        message = f"Line {closest_line_wavelength + 1} has the closest value: {closest_value_wavelength}"
        return closest_value_wavelength, message

def get_absorbance(nm):
    _, message = get_line_value(nm)
    line_number = int(message.split()[1]) - 1  # Subtract 1 because list indices start at 0

    with open(single_path, 'r') as file:
        lines = [line.strip() for line in file.readlines()]
        absorbance_value_select = lines[line_number]
        return absorbance_value_select
        

class SelectWavelength(QWidget):
    def __init__(self):
        super().__init__()
    


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
INTERPOLATE_FILE = os.getenv("INTERPOLATE_FILE")
PORT = os.getenv("PORT")
BAUDRATE = os.getenv("BAUDRATE")
baseline_path = os.path.join("data", BASELINE_FILE)
single_path = os.path.join("data", SINGLE_FILE)
wavelength_path = os.path.join("data", WAVELENGTH_FILE)
interpolate_path = os.path.join("data", INTERPOLATE_FILE)

def get_line_value(nm):
    with open(interpolate_path, 'r') as file:
        lines = [line.strip().split(',') for line in file.readlines()]
        # Convert strings to float
        lines = [(float(wavelength), float(absorbance)) for wavelength, absorbance in lines]
        # Find the line with the value closest to nm
        closest_line_wavelength = min(range(len(lines)), key=lambda index: abs(lines[index][0]-nm))
        closest_value_wavelength, closest_absorbance = lines[closest_line_wavelength]
        message = f"Line {closest_line_wavelength + 1} has the closest value: {closest_value_wavelength}"
        return closest_value_wavelength, message

def get_absorbance(nm):
    _, absorbance, _ = get_line_value(nm)
    return absorbance
        

class SelectWavelength(QWidget):
    def __init__(self):
        super().__init__()
    


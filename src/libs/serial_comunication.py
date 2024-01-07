import serial
import traceback
import time
from libs.log_util import config_logger

logger = config_logger()


class Serial:
    def __init__(self, port, baudrate=9600):
        """Inicializar la conexión en serie."""
        try:
            self.ser = serial.Serial(port, baudrate=baudrate)
            self.ser.flushInput()
            time.sleep(2) 
        except serial.SerialException as e:
            logger.error(e)

    def open(self):
        """Abrir la conexión en serie."""
        try:
            self.ser.open()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def close(self):
        """Cerrar la conexión en serie."""

        try:
            self.ser.close()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def read(self):
        """Leer los datos en serie y devolverlos."""

        try:
            data = self.ser.readline().decode().strip()
            return data
        except Exception as e:
            logger.error(e)

    def write(self, data):
        """Escribir los datos en serie."""
        try:
            self.ser.write(data)
        except Exception as e:
            logger.error(e)

    def flushInput(self):
        """Vaciar el buffer de entrada."""
        self.ser.flushInput()

    def flushOutput(self):
        """Vaciar el buffer de entrada."""
        self.ser.flushOutput()

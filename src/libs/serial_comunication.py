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
            logger.error(traceback.format_exc())

    def open(self):
        """Abrir la conexión en serie."""
        try:
            if not self.is_open():
                self.ser.open()
        except serial.SerialException as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def close(self):
        """Cerrar la conexión en serie."""
        try:
            if self.is_open():
                self.ser.close()
        except serial.SerialException as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def read(self):
        """Leer los datos en serie y devolverlos."""
        try:
            if self.is_open():
                data = self.ser.readline().decode().strip()
                return data

        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            return None

    def write(self, data):
        """Escribir los datos en serie."""
        try:
            if self.is_open():
                self.ser.write(data)
            else:
                logger.warning("WRITR-Trying to write to closed port.")
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def flushInput(self):
        """Vaciar el buffer de entrada."""
        try:
            if self.is_open():
                self.ser.flushInput()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def flushOutput(self):
        """Vaciar el buffer de salida."""
        try:
            if self.is_open():
                self.ser.flushOutput()
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())

    def is_open(self):
        """Verificar si el puerto está abierto."""
        return self.ser.isOpen()

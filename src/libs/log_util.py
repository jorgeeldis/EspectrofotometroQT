import logging
import sys


def config_logger():
    # Configuración del logger
    logger = logging.getLogger("espectrofotometer")
    logger.setLevel(logging.DEBUG)

    # Configuración del formato
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Configuración del manejador de consola
    consola_handler = logging.StreamHandler(stream=sys.stdout)
    consola_handler.setLevel(logging.INFO)
    consola_handler.setFormatter(formatter)
    consola_handler.encoding = sys.stdout.encoding

    # Configuración del manejador de archivo
    archivo_handler = logging.FileHandler("espectrofotometer.log", encoding='utf-8')
    archivo_handler.setLevel(logging.DEBUG)
    archivo_handler.setFormatter(formatter)

    # Agregar los manejadores al logger
    logger.addHandler(consola_handler)
    logger.addHandler(archivo_handler)

    return logger

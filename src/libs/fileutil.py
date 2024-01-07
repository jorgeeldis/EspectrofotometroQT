from libs.log_util import config_logger


logger = config_logger()


def write_data(file_name, data):
    """Escribir los datos en el archivo de texto."""
    try:
        with open(file_name, "a") as file:
            file.write(data)
            file.close()
    except Exception as e:
        logger.error(e)


def read_data(file_name):
    """Leer los datos del archivo de texto."""
    try:
        with open(file_name, "r") as file:
            data = file.read()
            file.close()
            return data
    except Exception as e:
        logger.error(e)

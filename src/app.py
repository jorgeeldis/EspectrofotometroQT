import sys
from libs.log_util import config_logger

from ui.main_window_app import init
logger = config_logger()

def main():
    logger.info("Iniciando la aplicación")
    init()


if __name__ == "__main__":
    main()

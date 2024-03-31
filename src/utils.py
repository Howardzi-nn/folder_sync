import logging
import sys
import os
import colorlog
import configparser

from datetime import datetime

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

config = configparser.ConfigParser()
config.read(f"{PROJECT_DIR}/settings.ini")
t = config.get("Setup", "log_level")


def setup_logging(log_file, console_logging=True):
    logger = logging.getLogger()
    logger.setLevel(config.get("Setup", "log_level"))

    formatter = colorlog.ColoredFormatter(
        "%(asctime)s - %(log_color)s%(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": 'cyan',
            "INFO": "green",
            'WARNING':  'yellow',
            'ERROR': 'red',
        },
        secondary_log_colors={},
        style='%'
    )

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(config.get('Setup', 'log_level'))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console_logging:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(
            config.get('Setup', 'log_level'))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def get_datetime_logname():
    return f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}.log'

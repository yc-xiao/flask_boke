"""
日志工具方法
"""
from colorlog import ColoredFormatter
from app.secure import LOG_FILE
import logging

def setup_logger(name, level=logging.DEBUG):
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - p%(process)s - {%(filename)s:%(lineno)d} - %(levelname)s - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        }
    )
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    file_handler = logging.FileHandler(LOG_FILE, 'a')
    handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


app_logger = setup_logger('app_logger')

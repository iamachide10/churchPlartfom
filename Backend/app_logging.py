import logging,os
from logging.handlers import RotatingFileHandler
from celery.utils.log import get_task_logger

def celery_logs():
    my_logger = get_task_logger("incoming_logs")
    my_logger.setLevel(logging.INFO)
    screen_display = logging.StreamHandler()
    screen_display.setLevel(logging.INFO)
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    screen_display.setFormatter(format)
    my_logger.addHandler(screen_display)
    my_logger.propagate=False
    return my_logger


def normal_logs():
    normal_logger = logging.getLogger("shark_logger")
    normal_logger.setLevel(logging.INFO)
    file_handler = logging.StreamHandler()
    file_handler.setLevel(logging.WARN)
    format = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(format)
    normal_logger.addHandler(file_handler)
    normal_logger.propagate=False
    return normal_logger


import logging

logging.basicConfig(level=logging.INFO)

def info(message):
    return logging.info(message)

def warn(message):
    return logging.warn(message)

def error(message):
    return logging.error(message)
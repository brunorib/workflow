import logging
import os

def switch(case):
   sw = {
      "INFO": logging.INFO,
      "DEBUG": logging.DEBUG,
      "ERROR": logging.ERROR,
   }
   return sw.get(case, logging.INFO)

logging.basicConfig(level=switch(os.getenv("LOG_LEVEL")))

def info(message):
    return logging.info(message)

def warn(message):
    return logging.warn(message)

def error(message):
    return logging.error(message)

def debug(message):
    return logging.debug(message)
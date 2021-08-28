import logging
import sys
import configparser

logger = logging.getLogger('root')

class Config:

    FILENAME = "config.ini"

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.read()

    def read(self):
        try:
            self.config.read(self.FILENAME)
        except configparser.Error:
            logger.critical("Config file does not exist")
            logger.info("ending application")
            sys.exit()

    def save(self):
        try:
            with open(self.FILENAME, 'w') as configfile:
                self.config.write(configfile)
        except configparser.Error:
            logger.critical("Writing the config file did fail")
            logger.info("ending application")
            sys.exit()

    def get(self, arg):
        try:
            return self.config["DEFAULT"][arg]
        except configparser.Error:
            logger.critical("The provided key (" + str(arg) + ") does not exist in the config file")
            logger.info("ending application")
            sys.exit()

    def set(self, **kwargs):
        for k,v in kwargs.items():
            self.config["DEFAULT"][k] = str(v)


config = Config()

def set_api_url(api_url):
    if isinstance(api_url, list):
        url = api_url[0]
    url = str(url)
    if not url.endswith("/"):
        url = url + "/"
    config.set(API_URL = url)
    config.save()

def set_log_level(log_level):
    config.set(LOG_LEVEL = log_level)
    config.save()
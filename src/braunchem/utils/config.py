from configparser import ConfigParser, ExtendedInterpolation

CONFIG = ConfigParser(interpolation=ExtendedInterpolation())


def load_config(config_path):
    global CONFIG
    CONFIG.read(config_path)

from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

CONFIG = ConfigParser(interpolation=ExtendedInterpolation())
"""Configurações."""

DATABASE_DIR = None
OUT_DIR = None
FOCUSES_DIR = None
TOPICS_DIR = None
PROBLEMS_DIR = None
IMAGES_DIR = None
TMP_DIR = None
TMP_PROBLEMS_DIR = None
TMP_TOPICS_DIR = None
TMP_IMAGES_DIR = None


def load_config(config_path):
    global CONFIG
    global DATABASE_DIR
    global OUT_DIR
    global FOCUSES_DIR
    global TOPICS_DIR
    global PROBLEMS_DIR
    global IMAGES_DIR
    global TMP_DIR
    global TMP_PROBLEMS_DIR
    global TMP_TOPICS_DIR
    global TMP_IMAGES_DIR

    CONFIG.read(config_path)

    DATABASE_DIR = Path(CONFIG["paths"]["database"])
    FOCUSES_DIR = Path(CONFIG["paths"]["focuses"])
    TOPICS_DIR = Path(CONFIG["paths"]["topics"])
    PROBLEMS_DIR = Path(CONFIG["paths"]["problems"])
    IMAGES_DIR = Path(CONFIG["paths"]["images"])

    OUT_DIR = Path(CONFIG["paths"]["out"])

    TMP_DIR = Path(CONFIG["paths"]["tmp"])
    TMP_PROBLEMS_DIR = TMP_DIR.joinpath("problems")
    TMP_TOPICS_DIR = TMP_DIR.joinpath("topics")
    TMP_IMAGES_DIR = TMP_DIR.joinpath("images")

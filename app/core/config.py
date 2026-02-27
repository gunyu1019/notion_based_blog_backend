import os

from configparser import ConfigParser
from app.utils.directory import directory


def get_config(name: str = "config") -> ConfigParser:
    parser = ConfigParser()
    parser.read(
        os.path.join(directory, "core", "{0}.ini".format(name)), encoding="utf-8"
    )
    return parser

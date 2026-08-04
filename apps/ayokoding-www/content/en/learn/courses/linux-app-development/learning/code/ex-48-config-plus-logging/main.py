"""Load configuration before configuring a logger."""

import configparser
import logging

config = configparser.ConfigParser()
config.read_dict({"logging": {"level": "INFO"}})
logging.basicConfig(
    level=getattr(logging, config["logging"]["level"]),
    format="%(levelname)s:%(message)s",
)
logging.info("configured notes daemon")

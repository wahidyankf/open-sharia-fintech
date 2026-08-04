"""Use logging levels to separate normal and verbose events."""

import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(message)s")
logging.debug("socket path resolved")
logging.info("daemon ready")
logging.warning("retrying connection")

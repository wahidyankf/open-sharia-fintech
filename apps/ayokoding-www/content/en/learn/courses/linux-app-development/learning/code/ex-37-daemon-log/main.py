"""Log daemon lifecycle events instead of printing them."""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logging.info("notes daemon started")
logging.info("notes daemon stopped")

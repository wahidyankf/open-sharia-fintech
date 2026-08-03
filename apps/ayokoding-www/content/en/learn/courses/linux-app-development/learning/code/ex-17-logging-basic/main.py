"""Emit one INFO record through Python logging."""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")
logging.info("notes daemon started")

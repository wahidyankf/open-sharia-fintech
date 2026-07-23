"""Example 52: dictConfig wires both modules' loggers to one formatted stream --
run this and find the bug from the correlated log lines alone, no breakpoints.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to dictConfig itself

import logging.config  # => co-05: dictConfig is the declarative, whole-tree way to wire every logger at once

import checkout  # => co-05: importing this ALSO imports inventory.py -- both loggers exist before dictConfig runs

LOGGING_CONFIG = {  # => co-05: ONE config wires BOTH modules' getLogger(__name__) instances at once
    "version": 1,  # => co-05: dictConfig's own required schema version, always 1
    "disable_existing_loggers": False,  # => co-05: keeps checkout/inventory's loggers alive after configuring
    "formatters": {  # => co-05: named formatters, referenced by name from handlers below
        "detailed": {
            "format": "%(asctime)s %(levelname)-7s %(name)-10s %(message)s",
            "datefmt": "%H:%M:%S",
        },  # => co-05: %(name)s is what makes each line correlatable back to its module
    },  # => co-05: closes the "formatters" mapping
    "handlers": {  # => co-05: named handlers, referenced by name from the root logger below
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "detailed",
            "level": "DEBUG",
        },  # => co-05: DEBUG here means the ROOT gate below decides the real floor
    },  # => co-05: closes the "handlers" mapping
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },  # => co-05: every module's logger inherits this UNLESS overridden
}  # => co-05: closes LOGGING_CONFIG -- one dict, both modules wired


def main() -> (
    None
):  # => co-05: drives two checkouts -- one that succeeds, one that hits the seeded bug
    logging.config.dictConfig(
        LOGGING_CONFIG
    )  # => co-05: applies the WHOLE config in one call, before any logging happens
    checkout.checkout(
        request_id="req-1", sku="SKU-100", qty=3, available=10
    )  # => co-05: req-1 -- expected to SUCCEED
    checkout.checkout(
        request_id="req-2", sku="SKU-200", qty=4, available=6
    )  # => co-05: req-2 -- qty=4 fits in available=6...


if (
    __name__ == "__main__"
):  # => co-05: guards the module-level call so importing this file stays side-effect-free
    main()  # => co-05: the ONE call whose output is read for the bug, with no breakpoints at all

"""Example 52: module B -- a SEPARATE per-module logger, correlated by request_id."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to logging itself

import logging  # => co-05: the SAME stdlib module inventory.py also uses, for a DIFFERENT logger name

import inventory  # => co-05: the OTHER module whose logger this example correlates against, by request_id

logger = logging.getLogger(
    __name__
)  # => co-05: name is "checkout", distinct from "inventory"


def checkout(
    request_id: str, sku: str, qty: int, available: int
) -> None:  # => co-05: request_id ties the two loggers together
    logger.info(
        "checkout START request_id=%s sku=%s qty=%s", request_id, sku, qty
    )  # => co-05: the FIRST correlated line
    # BUG: qty is silently doubled before being passed to reserve_stock (a
    # "reserve enough for a possible retry" idea that shipped without review).
    ok = inventory.reserve_stock(
        sku, qty * 2, available
    )  # => co-05: the BUG -- crosses into the OTHER module's logger
    if ok:  # => co-05: branches purely on inventory.py's own return value, no re-derivation of the rule
        logger.info(
            "checkout SUCCESS request_id=%s", request_id
        )  # => co-05: the SAME request_id closes the correlation
    else:  # => co-05: the branch req-2 below actually takes, once qty is silently doubled
        logger.error(
            "checkout FAILED request_id=%s sku=%s qty=%s available=%s",
            request_id,
            sku,
            qty,
            available,
        )  # => co-05

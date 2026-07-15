"""Example 52: module A -- per-module logger via getLogger(__name__)."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to logging itself

import logging  # => co-05: the stdlib module every per-module logger in this example is built from

logger = logging.getLogger(__name__)  # => co-05: name is "inventory", not "root"


def reserve_stock(
    sku: str, qty: int, available: int
) -> bool:  # => co-05: called from checkout.py, a SEPARATE module
    logger.info(
        "reserve_stock sku=%s qty=%s available=%s", sku, qty, available
    )  # => co-05: logged from "inventory"
    if qty > available:  # => the actual business rule this function enforces
        logger.warning(
            "reserve_stock DENIED sku=%s: requested %s exceeds available %s",
            sku,
            qty,
            available,
        )  # => co-05
        return False  # => co-05: the caller (checkout.py) is what turns this into a FAILED checkout
    logger.info(
        "reserve_stock OK sku=%s: reserved %s of %s", sku, qty, available
    )  # => co-05: the SUCCESS path's own line
    return True  # => co-05: the caller turns this into a SUCCESSFUL checkout

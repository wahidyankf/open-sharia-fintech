# learning/code/ex-30-docstring-to-api-doc/cart_api.py
"""ex-30: a typed, docstring-documented function -- the source of truth for its own API doc (co-17)."""  # => co-17: this file's own restated purpose, doubling as its module __doc__
#    every claim in this docstring is verified against the live signature by generate_api_doc.py

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic


def apply_gift_card(total: float, card_balance: float) -> float:  # => co-17: the fully typed public function under doc
    #    the Args/Returns sections below are the ONLY place this contract is written down
    """Apply a gift card's balance against a cart total.

    Args:
        total: the cart's pre-gift-card total, in dollars.
        card_balance: the gift card's remaining balance, in dollars.

    Returns:
        The amount still owed after the gift card is applied, never negative.
    """  # => co-17: this docstring is the ONLY place the contract is written -- generate_api_doc.py
    #    below reads it back programmatically, so there is no second, hand-duplicated copy anywhere
    return max(0.0, total - card_balance)  # => co-17: the balance never pushes the total below $0.00
    #    max(0.0, ...) is the guard -- a card_balance larger than total never produces a negative charge

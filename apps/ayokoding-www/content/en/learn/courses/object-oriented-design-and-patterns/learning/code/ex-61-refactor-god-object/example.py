"""Example 61: Refactor God Object.

co-33 (refactor to pattern): a god object mixing user validation, order pricing, and
receipt formatting is decomposed by applying co-01 (SRP) and co-06 (grasp-information-
expert) -- each responsibility moves to the class that already holds the data it
needs, and a locking test suite proves the decomposition preserves behavior.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# ============================================================
# BEFORE: one class doing validation, pricing, AND formatting
# ============================================================


class GodShop:  # => three unrelated responsibilities crammed into one class
    def __init__(self) -> None:  # => sets up the shared price dictionary used by all three responsibilities
        self.items: dict[str, float] = {}  # => item name -> unit price, used by pricing

    def add_item(self, name: str, price: float) -> None:  # => pricing-related setup
        self.items[name] = price  # => stores the price for later total() calls

    def is_valid_email(self, email: str) -> bool:  # => VALIDATION concern, unrelated to pricing/formatting
        return "@" in email and "." in email.split("@")[-1]  # => a minimal, deliberately simple check

    def total(self, item_names: list[str]) -> float:  # => PRICING concern
        return sum(self.items[name] for name in item_names)  # => sums the requested items' prices

    def format_receipt(self, item_names: list[str]) -> str:  # => FORMATTING concern
        lines = [f"{name}: ${self.items[name]:.2f}" for name in item_names]  # => one line per item
        lines.append(f"TOTAL: ${self.total(item_names):.2f}")  # => reuses total(), coupling formatting to pricing
        return "\n".join(lines)  # => the full receipt as one string


# ============================================================
# AFTER: three cohesive classes, one responsibility each
# ============================================================


class EmailValidator:  # => SRP: validation, and only validation
    def is_valid(self, email: str) -> bool:  # => identical logic to GodShop.is_valid_email, now isolated
        return "@" in email and "." in email.split("@")[-1]  # => same check, moved to its own home


@dataclass  # => auto-generates __init__ from the prices field below
class Catalog:  # => grasp-information-expert: Catalog owns the prices, so it computes totals
    prices: dict[str, float] = field(default_factory=dict)  # => item name -> unit price

    def add_item(self, name: str, price: float) -> None:  # => pricing-related setup, unchanged behavior
        self.prices[name] = price  # => same assignment as GodShop.add_item, now scoped to pricing only

    def total(self, item_names: list[str]) -> float:  # => information-expert: Catalog holds prices, so it sums them
        return sum(self.prices[name] for name in item_names)  # => identical formula to GodShop.total


class ReceiptFormatter:  # => SRP: formatting, and only formatting -- depends on Catalog, not the other way around
    def __init__(self, catalog: Catalog) -> None:  # => depends on Catalog rather than owning prices itself
        self.catalog = catalog  # => the one collaborator this class needs

    def format(self, item_names: list[str]) -> str:  # => identical output to GodShop.format_receipt
        lines = [f"{name}: ${self.catalog.prices[name]:.2f}" for name in item_names]  # => same per-line format
        lines.append(f"TOTAL: ${self.catalog.total(item_names):.2f}")  # => delegates pricing to Catalog, not itself
        return "\n".join(lines)  # => identical join to the god-object version


if __name__ == "__main__":  # => demonstration entry point, executed only when this file is run directly
    god = GodShop()  # => the original god object
    god.add_item("Book", 12.5)  # => registers a price on the god object
    god.add_item("Pen", 1.5)  # => registers a second price on the god object
    print(god.format_receipt(["Book", "Pen"]))  # => exercises all three responsibilities through one class
    # => Output: Book: $12.50
    # => Pen: $1.50
    # => TOTAL: $14.00

    catalog = Catalog()  # => the decomposed version
    catalog.add_item("Book", 12.5)  # => registers the same price on the decomposed Catalog
    catalog.add_item("Pen", 1.5)  # => registers the same second price on the decomposed Catalog
    formatter = ReceiptFormatter(catalog)  # => formatter depends on catalog, not the reverse
    print(formatter.format(["Book", "Pen"]))  # => identical output, now via three cohesive classes
    # => Output: Book: $12.50
    # => Pen: $1.50
    # => TOTAL: $14.00

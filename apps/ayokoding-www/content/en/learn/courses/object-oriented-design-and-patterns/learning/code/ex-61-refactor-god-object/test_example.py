"""Example 61: pytest verification that the god-object decomposition preserves behavior."""

from example import Catalog, EmailValidator, GodShop, ReceiptFormatter


def test_god_object_and_decomposed_version_produce_identical_receipts() -> None:
    god = GodShop()
    god.add_item("Book", 12.5)
    god.add_item("Pen", 1.5)
    catalog = Catalog()
    catalog.add_item("Book", 12.5)
    catalog.add_item("Pen", 1.5)
    formatter = ReceiptFormatter(catalog)
    assert god.format_receipt(["Book", "Pen"]) == formatter.format(["Book", "Pen"])  # => byte-identical output


def test_email_validation_is_identical_after_extraction() -> None:
    god = GodShop()
    validator = EmailValidator()  # => the extracted, standalone responsibility
    for email in ["a@b.com", "not-an-email", "x@y"]:  # => same three cases through both implementations
        assert god.is_valid_email(email) == validator.is_valid(email)  # => behavior is unchanged after extraction


def test_each_decomposed_class_has_exactly_one_responsibility() -> None:
    validator = EmailValidator()
    assert not hasattr(validator, "total")  # => EmailValidator knows nothing about pricing
    catalog = Catalog()
    assert not hasattr(catalog, "format")  # => Catalog knows nothing about formatting
    assert not hasattr(catalog, "is_valid")  # => Catalog knows nothing about validation


# => Run: pytest -q -- Output: 3 passed

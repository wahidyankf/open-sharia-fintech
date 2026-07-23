"""Example 53: pytest verification for Factory Method vs Abstract Factory."""

from example import PdfCreator, PdfSuiteFactory, WordCreator


def test_factory_method_varies_a_single_product() -> None:
    assert PdfCreator().open_document() == "opened a pdf document"
    assert WordCreator().open_document() == "opened a word document"


def test_abstract_factory_produces_a_matched_family_together() -> None:
    suite = PdfSuiteFactory()
    document_kind: str = suite.create_document().kind()
    toolbar_kind: str = suite.create_toolbar().kind()
    assert document_kind == "pdf"  # => both products
    assert toolbar_kind == "pdf-toolbar"  # => share the SAME family


# => Run: pytest -- Output: 2 passed

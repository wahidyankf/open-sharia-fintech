"""Example 74: pytest verification for Polymorphism via Duck Typing, with No Shared Base Class."""

from example import HtmlRenderer, MarkdownRenderer, render_all


def test_single_pipeline_handles_every_unrelated_renderer() -> None:
    output: list[str] = render_all("hi", [HtmlRenderer(), MarkdownRenderer()])
    assert output == ["<p>hi</p>", "**hi**"]  # => neither renderer shares a base class


# => Run: pytest -- Output: 1 passed

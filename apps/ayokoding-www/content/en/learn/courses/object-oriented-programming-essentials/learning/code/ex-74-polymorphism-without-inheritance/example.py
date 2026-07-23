"""Example 74: Polymorphism via Duck Typing, with No Shared Base Class."""


class HtmlRenderer:  # => begins the HtmlRenderer class body
    def render(
        self, text: str
    ) -> str:  # => no inheritance from any shared Renderer base
        return f"<p>{text}</p>"  # => returns this value to the caller


class MarkdownRenderer:  # => a second, entirely unrelated class
    def render(self, text: str) -> str:  # => same method NAME, structurally compatible
        return f"**{text}**"  # => returns this value to the caller


def render_all(
    text: str, renderers: list[object]
) -> list[str]:  # => a SINGLE shared pipeline
    return [r.render(text) for r in renderers]  # type: ignore


output: list[str] = render_all(
    "hi", [HtmlRenderer(), MarkdownRenderer()]
)  # => constructs output
print(output)  # => one pipeline call handled BOTH unrelated renderer types
# => Output: ['<p>hi</p>', '**hi**']
# => `render_all` never imports `HtmlRenderer` or `MarkdownRenderer`

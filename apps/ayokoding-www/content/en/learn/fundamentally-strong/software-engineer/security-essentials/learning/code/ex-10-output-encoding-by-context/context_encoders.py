# learning/code/ex-10-output-encoding-by-context/context_encoders.py
"""Example 10: Output Encoding by Context."""  # => co-06: module docstring

from __future__ import (
    annotations,
)  # => co-06: DD-39 hygiene, unrelated to the encoding itself

import json  # => co-06: json.dumps is a spec-correct JS-string-literal encoder -- NOT an HTML encoder

from markupsafe import (
    escape,
)  # => co-06: the correct encoder for HTML-body and HTML-attribute contexts


def html_body_encode(
    value: str,
) -> str:  # => co-06: correct encoder for text BETWEEN tags, e.g. <div>{}</div>
    """Encode a value for placement in an HTML text node."""  # => co-06: doc
    return str(escape(value))  # => co-06: turns <, >, &, quotes into HTML entities


def html_attr_encode(
    value: str,
) -> str:  # => co-06: correct encoder for a QUOTED attribute value
    """Encode a value for placement inside a quoted HTML attribute."""  # => co-06: doc
    return str(
        escape(value)
    )  # => co-06: SAME entity set also neutralizes quote-breakout from an attribute


def js_string_encode(
    value: str,
) -> str:  # => co-06: correct encoder for a JS STRING LITERAL, not HTML at all
    """Encode a value as a JS string literal -- escapes backslash and quotes JS-style, not HTML-style."""  # => co-06: doc
    return json.dumps(
        value
    )  # => co-06: JSON string syntax IS valid JS string syntax, backslash included


HTML_PAYLOAD = (
    '<b>bold</b> & "quoted"'  # => co-01: a value with HTML-special AND quote characters
)


if (
    __name__ == "__main__"
):  # => co-06: entry point -- three contexts, then the correct-vs-wrong JS comparison
    print("=== HTML-body context: <div>{}</div> ===")  # => co-06: context #1
    print(
        f"<div>{html_body_encode(HTML_PAYLOAD)}</div>"
    )  # => co-06: entities neutralize the <b> tag

    print(
        '\n=== HTML-attribute context: <input value="{}"> ==='
    )  # => co-06: context #2
    print(
        f'<input value="{html_attr_encode(HTML_PAYLOAD)}">'
    )  # => co-06: entities neutralize the embedded quote

    print(
        "\n=== JS-string context, CORRECT encoder (js_string_encode) ==="
    )  # => co-06: context #3, done right
    backslash_payload = "\\"  # => co-01: a single backslash -- the character HTML-encoding never touches
    right = "<script>var x = %s;</script>" % js_string_encode(
        backslash_payload
    )  # => co-06: json.dumps supplies its OWN quotes
    print(
        right
    )  # => co-06: a syntactically valid, properly-terminated JS string literal
    parsed = json.loads(
        right.split("var x = ")[1].rstrip(";</script>")
    )  # => co-06: parses the literal BACK as JSON
    print(
        f"round-trips to the original payload: {parsed == backslash_payload}"
    )  # => co-06: True -- correctly escaped

    print(
        "\n=== JS-string context, WRONG encoder (html_body_encode) ==="
    )  # => co-06: the context MISMATCH
    wrong_literal = '"%s"' % html_body_encode(
        backslash_payload
    )  # => co-06: HTML-encoding does NOT touch backslash
    wrong = (
        "<script>var x = %s;</script>" % wrong_literal
    )  # => co-06: the same backslash payload, wrong encoder
    print(
        wrong
    )  # => co-06: LOOKS plausible, but the trailing backslash escapes the closing quote
    try:  # => co-06: attempt to parse the SAME literal text as JSON, the way a correct one always would
        json.loads(
            wrong_literal
        )  # => co-06: this is where the mismatch is proven, not merely asserted
        print(
            "round-trips to the original payload: True"
        )  # => co-06: never reached -- parsing fails first
    except (
        json.JSONDecodeError
    ) as exc:  # => co-06: the mismatch: HTML-encoding alone left a MALFORMED JS string
        print(
            f"STILL BROKEN: {exc}"
        )  # => co-06: proves the wrong-context encoder leaves the string unterminated

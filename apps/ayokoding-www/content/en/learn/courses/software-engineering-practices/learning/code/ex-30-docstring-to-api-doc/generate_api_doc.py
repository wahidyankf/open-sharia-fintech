# learning/code/ex-30-docstring-to-api-doc/generate_api_doc.py
"""ex-30: generates a Markdown API reference page directly from cart_api.py's own signature and docstring (co-17)."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import inspect  # => co-17: stdlib-only -- inspect reads the REAL signature, never a hand-typed copy

#    no template engine or docstring-scraper dependency needed
from collections.abc import Callable  # => co-17: a precise, strict-mode-friendly type for "any callable", replacing a bare object

import cart_api  # => co-17: the module whose public function this script documents
#    -- the ONLY coupling between the two files is this one import


def render_api_doc(func: Callable[..., object]) -> str:  # => co-17: builds one Markdown section from a function object
    """Render one function's live signature and docstring as a Markdown API-reference section."""  # => co-17: documents render_api_doc's contract -- no runtime output, just sets its __doc__
    name: str = getattr(func, "__name__", repr(func))  # => co-17: Callable has no statically-known __name__ -- getattr with a str default keeps this strict-mode clean
    signature = inspect.signature(func)  # => co-17: the REAL, current parameter names, types, and return annotation
    doc = inspect.getdoc(func) or ""  # => co-17: the REAL docstring, dedented -- not retyped by hand anywhere
    return f"### `{name}{signature}`\n\n{doc}\n"  # => co-17: one Markdown section, entirely derived, zero hand-duplication
    #    if cart_api.py's docstring ever changes, this output changes too


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    doc_page = render_api_doc(cart_api.apply_gift_card)  # => co-17: the actual generation call this example demonstrates
    print(doc_page)  # => co-17: prints the generated Markdown section

    live_signature = str(inspect.signature(cart_api.apply_gift_card))  # => co-17: re-reads the signature independently
    #    of render_api_doc, for a truly independent check
    assert live_signature in doc_page, "generated doc must contain the function's REAL signature"  # => co-17: the check
    assert "never negative" in doc_page, "generated doc must contain the REAL docstring body"  # => co-17: the check
    #    -- proves the doc came
    #    from the docstring, not a stub
    print("Generated doc matches the live signature and docstring, no hand-duplicated copy: True")  # => co-17: reached only if both asserts passed

"""Example 58: Pydantic Custom Types via Annotated.

Annotated[..., Field(...)] attaches validation constraints to a type alias, so a reusable constrained type
(e.g. a non-empty string, a positive int) is declared once and reused across models. Run: python3 example.py.
(co-12, co-13)
"""

from typing import Annotated  # => Annotated attaches metadata (constraints) to a type (co-12)

from pydantic import BaseModel, Field


# => a reusable constrained type: a non-empty string of at most 100 chars (co-13)
NonEmptyStr = Annotated[str, Field(min_length=1, max_length=100)]  # => declared ONCE, reused below


class Article(BaseModel):  # => a model using the constrained type
    title: NonEmptyStr  # => reuses NonEmptyStr -- the constraint applies here too (co-12)
    body: NonEmptyStr  # => and here -- one definition, two uses


def main() -> None:  # => demonstrates the constraint enforcing on both fields
    good = Article(title="Hello", body="World")  # => both non-empty -> accepted
    print(good.model_dump())  # => Output: {'title': 'Hello', 'body': 'World'}
    import pydantic  # => to catch the ValidationError

    try:
        Article(title="", body="ok")  # => empty title violates min_length=1 (co-13)
        raised = False
    except pydantic.ValidationError:
        raised = True
    print(raised)  # => Output: True -- the constrained type rejected the empty title


if __name__ == "__main__":  # => run directly
    main()

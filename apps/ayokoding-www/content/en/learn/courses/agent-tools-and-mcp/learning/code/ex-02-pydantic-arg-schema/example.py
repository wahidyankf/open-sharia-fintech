# TypedDict is a standard-library stand-in for a Pydantic-derived schema.
from typing import TypedDict


# This type documents the single accepted input field.
class WeatherArgs(TypedDict):
    # A city must be represented as text.
    city: str


# The validator models what a Pydantic boundary would enforce.
def validate(raw: dict[str, object]) -> WeatherArgs:
    # Reject absent or non-string values before a handler is called.
    if not isinstance(raw.get("city"), str):
        raise ValueError("city must be a string")
    # Return the narrowed typed shape after validation.
    return {"city": raw["city"]}


# A valid local request needs no provider credentials.
assert validate({"city": "Jakarta"}) == {"city": "Jakarta"}
# A missing required field proves the schema boundary works.
try:
    validate({})
except ValueError as error:
    print(error)

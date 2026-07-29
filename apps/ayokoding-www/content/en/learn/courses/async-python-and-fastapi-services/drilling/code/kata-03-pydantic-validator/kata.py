"""Kata 3 -- A Pydantic validator that rejects a bad value (co-12, co-13)."""

import pydantic  # => to catch ValidationError
from pydantic import (
    BaseModel,
    field_validator,
)  # => co-12: field_validator is the custom-rule verb


class User(BaseModel):  # => a model with a custom email rule (co-12)
    email: str  # => a plain string at the type level

    @field_validator("email")  # => the custom rule runs during validation (co-13)
    @classmethod
    def must_have_at(cls, value: str) -> str:  # => receives the raw value
        if "@" not in value:  # => the rule
            raise ValueError(
                "email must contain '@'"
            )  # => a violation -> ValidationError/422 (co-13)
        return value  # => accepted value


def main() -> None:
    ok = User(email="a@b.com")  # => accepted
    print(ok.email)  # => Output: a@b.com
    try:
        User(email="bad")  # => no @ -> rejected (co-13)
        raised = False
    except pydantic.ValidationError:
        raised = True
    print(raised)  # => Output: True
    assert raised is True


if __name__ == "__main__":
    main()

"""Example 57: Pydantic Serialization Aliases.

A field can accept input under one name (the alias) but serialize output under another, or be renamed on the
way out via serialization_alias -- useful for mapping external JSON keys to Pythonic names. Run: python3 example.py.
(co-12, co-14)
"""

from pydantic import BaseModel, Field


class User(BaseModel):  # => a model whose input/output keys differ from the field name (co-14)
    # => validation_alias: accept input as "firstName"; the field is still .first_name in Python (co-12)
    first_name: str = Field(validation_alias="firstName")  # => external JSON uses camelCase
    # => serialization_alias: emit the field as "familyName" in model_dump() output (co-14)
    family_name: str = Field(serialization_alias="familyName")  # => Python field differs from JSON key


def main() -> None:  # => demonstrates input-by-alias and output-by-alias
    user = User.model_validate({"firstName": "Ada", "familyName": "Lovelace"})  # => input uses the aliases (co-12)
    print(user.first_name, user.family_name)  # => Pythonic access: Ada Lovelace
    dumped = user.model_dump(by_alias=True)  # => serialize WITH aliases -- JSON-shaped keys (co-14)
    print(dumped)  # => Output: {'firstName': 'Ada', 'familyName': 'Lovelace'}


if __name__ == "__main__":  # => run directly
    main()

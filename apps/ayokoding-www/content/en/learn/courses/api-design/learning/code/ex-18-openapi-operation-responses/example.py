# pyright: strict
"""Example 18: Declaring 200/404/422 per Operation. (co-09)

Every response status an operation can actually return belongs in its
`responses` object -- not just the happy path. This example declares
200/404/422 for one operation and confirms each is documented.
"""

from typing import Any  # => an operation object is arbitrary nested JSON

OPERATION: dict[str, Any] = {  # => co-09: one GET operation's full response contract
    "summary": "Get an article by id",  # => a human-readable one-liner
    "responses": {  # => every status this operation can legally return
        "200": {"description": "the article was found"},  # => the happy path
        "404": {"description": "no article exists with that id"},  # => co-07's not-found case
        "422": {"description": "the id path parameter was not a valid integer"},  # => co-07's 422 case
    },  # => end of the responses block
}  # => end of OPERATION
# => OPERATION["responses"] has exactly 3 keys: "200", "404", "422"

EXPECTED_CODES = ("200", "404", "422")  # => co-09: the three outcomes this operation can produce

declared_codes = tuple(OPERATION["responses"].keys())  # => what the spec ACTUALLY documents
# => declared_codes is ('200', '404', '422') (type: tuple[str, ...])
print(f"declared response codes: {declared_codes}")  # => Output: ('200', '404', '422')

missing_codes = [code for code in EXPECTED_CODES if code not in OPERATION["responses"]]  # => the gap check
# => co-09: any expected code ABSENT from the spec is an undocumented behavior
print(f"undocumented expected codes: {missing_codes}")  # => Output: [] -- all three are documented

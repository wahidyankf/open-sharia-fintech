"""Example 17: allow-list a stable application identifier."""

from __future__ import (
    annotations,
)  # => Enables modern annotations without changing validation.

import re  # => A full-match pattern makes the accepted language explicit.

PROJECT_ID = re.compile(
    r"[a-z][a-z0-9-]{2,31}"
)  # => Only lowercase project IDs are accepted.


def parse_project_id(
    value: str,
) -> str:  # => Boundary function accepts text from an untrusted request.
    if not PROJECT_ID.fullmatch(
        value
    ):  # => Rejects everything outside the documented format.
        raise ValueError(
            "project ID must be 3–32 lowercase letters, digits, or hyphens"
        )  # => Safe, generic error.
    return value  # => Downstream code receives an already constrained value.


if __name__ == "__main__":  # => A local, deterministic demonstration.
    print(parse_project_id("ledger-api"))  # => Expected accepted project identifier.
    try:  # => Demonstrate the rejection path without invoking a shell or network.
        parse_project_id("ledger;rm")  # => The semicolon is not in the allow-list.
    except ValueError as error:  # => Expected failure is handled as input validation.
        print(error)  # => Prints the generic validation message.

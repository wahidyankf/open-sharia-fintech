"""Example 23: normalized request method."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    raw_method: str

    @property
    def method(self) -> str:
        # => Normalizing once gives handlers a stable representation.
        return self.raw_method.upper()


def main() -> None:
    # => Lowercase input becomes the protocol-standard uppercase method.
    print(Request("get").method)


if __name__ == "__main__":
    main()

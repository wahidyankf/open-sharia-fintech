"""Example 61: argparse CLI with a Positional Argument."""

import argparse  # => imports the standard-library CLI-parsing module


def main() -> None:  # => defines the entry point, called only when run directly
    parser = argparse.ArgumentParser(description="Greet someone by name.")
    # => creates a parser; description shows up in the auto-generated --help text
    # A required positional argument -- no leading dashes.
    parser.add_argument("name", type=str, help="the name to greet")
    args = parser.parse_args()  # => parses sys.argv -- args.name holds the value
    print(f"Hello, {args.name}")  # => prints the greeting using the parsed name


if __name__ == "__main__":  # => True only when cli.py is run directly, not imported
    main()  # => calls main(), which builds the parser and prints the greeting
# => Run: python3 cli.py Ada -- Output: Hello, Ada

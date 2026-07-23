"""Example 63: argparse -h/--help."""

import argparse  # => imports the standard-library CLI-parsing module


def main() -> None:  # => defines the entry point, called only when run directly
    # prog fixes the shown program name, regardless of the real filename.
    parser = argparse.ArgumentParser(
        prog="cli.py",  # => overrides sys.argv[0] in the usage/help text
        description="Greet someone by name.",  # => shown at the top of --help output
    )  # => closes ArgumentParser(...)
    parser.add_argument("name", type=str, help="the name to greet")
    # argparse auto-generates -h/--help -- no code needed for it.
    # parse_args() itself exits before returning if -h/--help was passed.
    args = parser.parse_args()
    print(f"Hello, {args.name}")  # => prints the greeting using the parsed name


if __name__ == "__main__":  # => True only when cli.py is run directly, not imported
    main()  # => calls main(), which builds the parser and prints the greeting
# => Run: python3 cli.py -h -- prints a usage block and exits 0

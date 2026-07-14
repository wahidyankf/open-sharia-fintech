"""Example 82: a module with a top docstring and a main() under the name guard."""


def main() -> None:  # => defines the entry point, only called under the guard below
    print("app module running")  # => Output (only on direct run): app module running


if __name__ == "__main__":  # => True only when app.py is run directly, not imported
    main()  # => calls main(), printing the line above
# => `python3 -c "import app; print(app.__doc__)"` prints this file's top docstring,
# => and never runs main() -- importing never triggers the name guard

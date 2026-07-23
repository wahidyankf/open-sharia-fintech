"""Example 46: __name__ == "__main__" Guard."""


def main() -> None:  # => defines the entry-point function
    print("running as a script")  # => Output (only on direct run)


# __name__ is "__main__" only when run directly, never when imported.
if __name__ == "__main__":  # => True only when this file is executed directly
    main()  # => calls main(), which prints the line above

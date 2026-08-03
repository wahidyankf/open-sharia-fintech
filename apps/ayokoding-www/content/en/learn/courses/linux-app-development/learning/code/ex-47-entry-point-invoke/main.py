"""Invoke the callable used by a console-script entry point."""


def main(argv: list[str]) -> int:
    print(f"notes command: {argv[0]}")
    return 0


assert main(["status"]) == 0

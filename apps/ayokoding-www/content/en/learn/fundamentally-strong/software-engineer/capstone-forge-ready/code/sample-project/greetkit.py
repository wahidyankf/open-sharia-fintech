"""greetkit -- a tiny greeting library, the capstone's sample Python project."""


def build_message(nam: str) -> str:
    """Build a greeting message for nam."""
    if not nam:
        nam = "World"
    return f"Hello, {nam}!"


def shout_message(nam: str) -> str:
    """Build an all-caps greeting message for nam."""
    return build_message(nam).upper()

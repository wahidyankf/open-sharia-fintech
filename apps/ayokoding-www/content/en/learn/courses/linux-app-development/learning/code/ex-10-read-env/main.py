"""Read a process environment variable."""

import os

print(os.environ["NOTES_MODE"] if "NOTES_MODE" in os.environ else "unset")

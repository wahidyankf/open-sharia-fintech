"""Use a safe environment fallback."""

import os

print(os.environ.get("NOTES_MODE", "development"))

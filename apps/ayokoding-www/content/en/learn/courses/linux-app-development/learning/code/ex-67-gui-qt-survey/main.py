"""Survey Qt availability without making it a core dependency."""

import importlib.util

available = importlib.util.find_spec("PySide6") is not None
print(f"Qt available: {available}; Qt is suitable for cross-desktop Linux GUIs.")

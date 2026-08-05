"""Survey GTK availability without making it a core dependency."""

import importlib.util

available = importlib.util.find_spec("gi") is not None
print(f"GTK available: {available}; GTK is suitable for GNOME-native Linux GUIs.")

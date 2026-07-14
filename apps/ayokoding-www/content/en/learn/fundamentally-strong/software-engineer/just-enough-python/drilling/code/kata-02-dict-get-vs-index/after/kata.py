"""Kata 2 (after): .get() with an explicit default."""

settings: dict[str, str] = {"theme": "dark"}
print(settings.get("timeout", "30"))

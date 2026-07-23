"""Example 76: Nested Dict Access with Chained .get(...)."""

config: dict[str, dict[str, str]] = {"server": {"host": "localhost"}}
# => config has one top-level key "server", itself a dict with "host"

# .get(key, default) never raises KeyError -- it falls back to default instead.
port = config.get("server", {}).get("port", "8080")
# => first .get() finds "server"; second .get() finds no "port" key, so falls back
print(port)  # => Output: 8080

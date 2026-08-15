# A dataclass makes the advertised tool contract inspectable.
from dataclasses import dataclass


# Immutable metadata prevents a handler from silently changing its identity.
@dataclass(frozen=True)
class Tool:
    # The model selects this stable operation name.
    name: str
    # The description explains when the tool applies.
    description: str
    # Required fields are the typed input boundary.
    required: tuple[str, ...]


# This local tool has no credential or network dependency.
weather = Tool("weather", "Get current weather for one city", ("city",))
# The assertions make the advertised schema executable documentation.
assert weather.name == "weather" and weather.required == ("city",)
# The observable output is the contract a client can discover.
print(weather)

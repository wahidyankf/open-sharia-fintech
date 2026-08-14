# Tool descriptions are model-facing selection hints.
from dataclasses import dataclass


# The fake model considers words in the task and description.
@dataclass(frozen=True)
class Tool:
    # Names make the result observable.
    name: str
    # Descriptions supply the selection evidence.
    description: str


# This deterministic selector rewards a relevant description.
def choose(task: str, tools: list[Tool]) -> Tool:
    # Prefer the tool that explicitly mentions the task noun.
    return max(tools, key=lambda tool: int("weather" in tool.description.lower()))


# The vague tool has no use-case signal.
bad = Tool("lookup", "Gets information")
# The focused tool explains when it should be called.
good = Tool("weather", "Get weather forecasts for a city")
# The fake model makes the description comparison repeatable.
assert choose("weather in Jakarta", [bad, good]) == good
# The selected name is the learner-visible result.
print(good.name)

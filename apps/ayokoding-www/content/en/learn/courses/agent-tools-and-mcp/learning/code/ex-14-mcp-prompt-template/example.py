# Prompt templates are server-provided reusable instructions.
from dataclasses import dataclass


# A template contains a named parameter slot.
@dataclass(frozen=True)
class Prompt:
    # The name lets a client discover the prompt.
    name: str
    # The template remains data until a client requests it.
    template: str


# This prompt is local, deterministic, and non-executable.
greeting = Prompt("greet-user", "Greet {name} warmly.")
# Formatting supplies a typed task value at fetch time.
rendered = greeting.template.format(name="Ada")
# The assertion verifies the parameterized prompt contract.
assert rendered == "Greet Ada warmly."
# Print the reusable instruction content.
print(rendered)

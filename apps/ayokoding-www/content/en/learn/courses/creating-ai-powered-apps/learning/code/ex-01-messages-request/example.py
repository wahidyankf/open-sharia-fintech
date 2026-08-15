from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str


response = Message("assistant", "mock response")
assert response.role == "assistant"
print("PASS: messages-request")

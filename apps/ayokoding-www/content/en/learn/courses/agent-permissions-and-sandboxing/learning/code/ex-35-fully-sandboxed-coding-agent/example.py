"""Offline advanced guardrail 35."""


def permitted(profile: str, action: str) -> bool:
    # => Production denies unsafe actions even when exploration permits them.
    return profile == "explore" and action == "reversible"


def main() -> None:
    # => The simulated harness proves policy without touching host resources.
    assert not permitted("production", "unsafe")
    print("PASS: fully-sandboxed-coding-agent")


if __name__ == "__main__":
    main()

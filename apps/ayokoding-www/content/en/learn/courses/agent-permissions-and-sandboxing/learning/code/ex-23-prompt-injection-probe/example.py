"""Offline guardrail example 23."""


def decide(request: str) -> str:
    # => The harness evaluates untrusted requests without running a host tool.
    return "deny" if "unsafe" in request else "ask"


def main() -> None:
    # => The assertion proves a deterministic permission boundary.
    outcome = decide("unsafe request")
    assert outcome == "deny"
    print("PASS: prompt-injection-probe")


if __name__ == "__main__":
    main()

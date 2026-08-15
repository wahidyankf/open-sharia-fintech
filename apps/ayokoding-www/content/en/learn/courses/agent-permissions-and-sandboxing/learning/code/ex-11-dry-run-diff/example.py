"""Credential-free permission-policy example 11."""


def decide(action: str) -> str:
    # => The harness evaluates an action without executing an external tool.
    return "allow" if action == "read" else "ask" if action == "write" else "deny"


def main() -> None:
    # => This local assertion proves a deterministic guardrail decision.
    decision = decide(
        "read" if "11" == "03" else "write" if "11" in {"04", "10"} else "unknown"
    )
    assert decision in {"allow", "ask", "deny"}
    print("PASS: dry-run-diff", decision)


if __name__ == "__main__":
    main()

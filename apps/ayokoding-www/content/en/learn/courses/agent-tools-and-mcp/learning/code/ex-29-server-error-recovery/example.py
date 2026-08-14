# Typed errors give the client a recovery signal.
def primary() -> dict[str, str]:
    # This simulated server failure is returned as data.
    return {"ok": "false", "code": "UNAVAILABLE"}


# The client selects a safe local fallback after inspection.
def recover() -> str:
    # Recovery reads the error rather than guessing.
    if primary()["code"] == "UNAVAILABLE":
        return "cached-result"
    # A successful primary would be handled differently.
    return "primary-result"


# The deterministic failure exercises the fallback branch.
assert recover() == "cached-result"
# Print the recovered result.
print(recover())

# An allow-list turns a shell-shaped tool into a narrow contract.
ALLOWED = {"status", "version"}


# Validation happens before any subprocess could be considered.
def run(command: str) -> str:
    # Unlisted commands are blocked as data, not executed.
    if command not in ALLOWED:
        return "blocked"
    # Local output simulates an approved safe operation.
    return f"ran:{command}"


# The policy permits one explicit safe command.
assert run("status") == "ran:status"
# The policy rejects destructive-looking input.
assert run("rm") == "blocked"
# Print the blocked outcome.
print(run("rm"))

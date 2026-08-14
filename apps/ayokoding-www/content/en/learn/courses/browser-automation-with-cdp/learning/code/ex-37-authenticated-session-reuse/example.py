"""Example 37: reuse a synthetic authenticated fixture session."""

# => This synthetic value models a fixture session and is never a real credential.
session = {"cookie": "fixture-session", "logins": 1}
# => Pages consume the same owned session rather than performing another login.
pages = [session["cookie"], session["cookie"]]
# => Reuse preserves the session identity and prevents duplicate login work.
assert pages == ["fixture-session", "fixture-session"] and session["logins"] == 1
# => Output reports the reuse policy without exposing a secret value.
print("fixture session reused")

"""Example 71: invalidate stale sessions after a fixture browser restart."""

# => A browser restart makes the previous session identifier unusable.
session = {"id": "old-session", "valid": False}
# => Reattachment creates a new session only after the stale one is recognized.
if not session["valid"]:
    session = {"id": "new-session", "valid": True}
# => The assertion proves recovery does not continue with a stale session id.
assert session == {"id": "new-session", "valid": True}
# => Output records successful reattachment after restart.
print("reattached after browser restart")

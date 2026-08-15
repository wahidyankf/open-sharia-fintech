"""Example 20: fill a local form fixture and assert its submitted value."""

# => Keep form state local so the demonstration has no account or network side effect.
form = {"email": "", "submitted": False}
# => Typing changes the same field that the later submit operation will validate.
form["email"] = "reader@example.test"
# => Submission succeeds only after the required fixture value exists.
form["submitted"] = bool(form["email"])
# => Assert the user-visible outcome, not merely that an input event was issued.
assert form == {"email": "reader@example.test", "submitted": True}
# => Output records the deterministic local form result.
print("form submitted")

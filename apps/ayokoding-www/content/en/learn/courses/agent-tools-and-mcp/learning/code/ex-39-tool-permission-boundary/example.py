# Policy names the only authorized capability.
allowed = {"read"}


# The boundary evaluates policy before dispatch.
def call(name: str) -> str:
    # An unapproved call becomes typed feedback.
    return "ok" if name in allowed else "DENIED"


# The denied action never reaches a handler.
assert call("write") == "DENIED"
# Print the policy result.
print(call("write"))

# Validation happens before an effectful handler is reached.
ALLOWED = {"city"}


# The handler would be the only place an action could occur.
def weather(args: dict[str, str]) -> str:
    # This local return is intentionally harmless.
    return f"weather for {args['city']}"


# The boundary rejects unknown fields, not only missing ones.
def call(args: dict[str, str]) -> str:
    # Extra keys may signal a mismatched or malicious call.
    if set(args) - ALLOWED:
        raise ValueError("unexpected argument")
    # Only validated data is passed to the handler.
    return weather(args)


# The invalid call proves the handler cannot run with an extra argument.
try:
    call({"city": "Jakarta", "shell": "rm"})
except ValueError as error:
    print(error)

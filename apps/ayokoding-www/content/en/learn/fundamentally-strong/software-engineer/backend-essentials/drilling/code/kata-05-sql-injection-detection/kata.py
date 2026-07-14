def build_unsafe_query(status: str) -> str:  # => co-14/co-20: string-concatenated -- the INJECTION-UNSAFE way
    return f"SELECT * FROM tasks WHERE status = '{status}'"  # => user input lands DIRECTLY in the SQL text


def build_safe_query(status: str) -> tuple[str, tuple[str, ...]]:  # => co-14: parameterized -- the SAFE way
    return "SELECT * FROM tasks WHERE status = ?", (status,)  # => the driver binds params, never concatenates


def is_injection_attempt(user_input: str) -> bool:  # => a crude but effective mocked detector for this kata
    suspicious = ["'", "--", ";", " OR ", " or "]  # => classic single-quote breakout + comment + stacking
    return any(token in user_input for token in suspicious)


malicious_input = "done' OR '1'='1"  # => a classic SQL-injection payload targeting the status filter

unsafe_sql = build_unsafe_query(malicious_input)  # => the payload becomes part of the SQL TEXT itself
safe_sql, safe_params = build_safe_query(malicious_input)  # => the payload stays DATA, never SQL syntax

print(unsafe_sql)  # => Output: SELECT * FROM tasks WHERE status = 'done' OR '1'='1'
print(safe_sql, safe_params)  # => Output: SELECT * FROM tasks WHERE status = ? ("done' OR '1'='1",)

# => the unsafe query's WHERE clause now ALWAYS matches every row -- the injection succeeded structurally
assert "OR '1'='1'" in unsafe_sql  # => the payload escaped the intended string literal boundary
# => the safe query's placeholder never changes shape -- the payload is inert, quoted DATA, not code
assert safe_sql == "SELECT * FROM tasks WHERE status = ?"  # => structurally IDENTICAL regardless of input
assert safe_params == (malicious_input,)  # => the whole payload is just one opaque bound parameter

assert is_injection_attempt(malicious_input) is True  # => flags the suspicious payload
assert is_injection_attempt("done") is False  # => a normal, benign filter value passes through clean
print("kata-05 OK")

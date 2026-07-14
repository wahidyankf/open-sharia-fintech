# => co-02: RFC 9110's idempotent set -- repeating the same call any number of times has the SAME effect
IDEMPOTENT_METHODS: frozenset[str] = frozenset({"GET", "HEAD", "PUT", "DELETE", "OPTIONS", "TRACE"})


def is_idempotent(method: str) -> bool:  # => O(1) average membership test against the frozen set
    return method.upper() in IDEMPOTENT_METHODS  # => normalize case -- HTTP methods are conventionally upper


def safe_to_blind_retry(method: str) -> bool:  # => the practical consequence a client relies on
    return is_idempotent(method)  # => co-02: only idempotent methods are safe to retry without side effects


methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]  # => the five methods this topic teaches
results = {m: is_idempotent(m) for m in methods}  # => one idempotency verdict per method
print(results)  # => Output: {'GET': True, 'POST': False, 'PUT': True, 'PATCH': False, 'DELETE': True}

assert results["POST"] is False  # => co-02: POST is explicitly NOT idempotent -- two POSTs can create two rows
assert results["PATCH"] is False  # => RFC 5789: PATCH is "neither safe nor idempotent"
assert results["PUT"] is True  # => PUT "created or replaced" -- repeating it converges to the same state
assert safe_to_blind_retry("GET") is True  # => reads are always safe to retry blindly
assert safe_to_blind_retry("POST") is False  # => a client library must NOT blindly retry a bare POST
print("kata-07 OK")

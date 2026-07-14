def classify_status(code: int) -> str:  # => co-03: RFC 9110 groups status codes into five classes
    if 200 <= code < 300:  # => 2xx: the request succeeded
        return "success"
    if 300 <= code < 400:  # => 3xx: further action (redirect) needed
        return "redirect"
    if 400 <= code < 500:  # => 4xx: the CLIENT made a mistake (bad body, missing auth, wrong path)
        return "client-error"
    if 500 <= code < 600:  # => 5xx: the SERVER failed to fulfil a valid request
        return "server-error"
    raise ValueError(f"not a valid HTTP status code: {code}")  # => outside 200-599 isn't a status class at all


codes = [200, 201, 204, 301, 400, 401, 404, 405, 422, 500]  # => the exact status set this topic teaches
classes = [classify_status(c) for c in codes]  # => one class label per code, same order
print(classes)  # => Output: ['success', 'success', 'success', 'redirect', 'client-error', 'client-error', 'client-error', 'client-error', 'client-error', 'server-error']

assert classify_status(201) == "success"  # => 201 Created -- a successful POST (co-02)
assert classify_status(422) == "client-error"  # => Unprocessable Content, native to RFC 9110 (co-10/co-11)
assert classify_status(500) == "server-error"  # => an unhandled exception, never a stack trace (co-11)
print("kata-02 OK")

# pyright: strict
"""Example 28: Correlation ID -- thread one id through every log line. (co-25)

A correlation (request) id is minted at the request boundary and carried on
EVERY log line the request produces, so all of a request's lines group
together in a log aggregator -- across functions, across services.
"""

import json  # => stdlib: each log line is a JSON object


LOG_BUFFER: list[str] = []  # => collects the request's lines, so we can inspect them together


def log(level: str, message: str, request_id: str) -> None:  # => co-25: every line carries the SAME request_id
    LOG_BUFFER.append(json.dumps({"level": level, "message": message, "request_id": request_id}))  # => stamped with the id


def handle_request(request_id: str) -> None:  # => a request's lifetime, all lines sharing the id
    log("info", "received request", request_id)  # => entry line, stamped
    validate(request_id)  # => a deeper function still threads the SAME id
    log("info", "request complete", request_id)  # => exit line, stamped


def validate(request_id: str) -> None:  # => a nested call -- still carries the id down
    log("debug", "validating payload", request_id)  # => co-25: the id propagates across function boundaries


handle_request("req-xyz-789")  # => one request, three lines, one shared id
for line in LOG_BUFFER:  # => print every line the request produced
    print(line)  # => Output: three JSON lines, all carrying request_id=req-xyz-789

parsed = [json.loads(line) for line in LOG_BUFFER]  # => parse them all back
all_carry_id = all(entry["request_id"] == "req-xyz-789" for entry in parsed)  # => co-25: every line carries the id
print(f"every line carries the correlation id: {all_carry_id}")  # => Output: True
assert all_carry_id and len(LOG_BUFFER) == 3  # => co-25: three lines, one shared id throughout

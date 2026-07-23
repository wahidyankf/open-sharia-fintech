"""Example 46: hammers the live app.py login endpoint -- the Nth rapid request gets a real 429 (co-27)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the hammering loop itself

import requests  # => co-27: real HTTP client -- every request below hits the live app.py process

BASE_URL = (
    "http://127.0.0.1:5046"  # => co-27: matches app.py's app.run(port=5046) exactly
)


def main() -> (
    None
):  # => co-27: fires 7 real rapid requests against a limit of "5 per minute"
    for attempt in range(
        1, 8
    ):  # => co-27: one more attempt than the limit -- guarantees at least one 429
        response = requests.post(
            f"{BASE_URL}/login", timeout=5
        )  # => co-27: a REAL HTTP POST, no delay between calls
        print(
            f"attempt {attempt}: status={response.status_code} body={response.text.strip()}"
        )  # => real, per-attempt
        if attempt <= 5:  # => co-27: the first 5 requests are within the declared limit
            assert (
                response.status_code == 200
            )  # => co-27: proves the limiter allows traffic UNDER the threshold
        else:  # => co-27: requests 6 and 7 exceed the "5 per minute" rule
            assert (
                response.status_code == 429
            )  # => co-27: proves the limiter really throttles traffic OVER it


if (
    __name__ == "__main__"
):  # => co-27: only runs when launched directly, e.g. `python3 hammer.py`
    main()  # => co-27: fires all 7 real requests and asserts the exact 200/429 boundary at attempt 6

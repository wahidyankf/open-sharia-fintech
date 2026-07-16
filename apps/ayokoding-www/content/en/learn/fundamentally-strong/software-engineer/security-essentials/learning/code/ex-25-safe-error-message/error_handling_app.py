# learning/code/ex-25-safe-error-message/error_handling_app.py
"""Example 25: Safe Error Message."""  # => co-23: module docstring

from __future__ import (
    annotations,
)  # => co-23: DD-39 hygiene, unrelated to error handling itself

import io  # => co-22: an in-memory stream stands in for a real log file/aggregator
import logging  # => co-22: the server-side channel the real traceback belongs in, never the client response
import traceback  # => co-23: traceback.format_exc() -- what the VULNERABLE handler leaks to the client

from flask import (
    Flask,
    jsonify,
)  # => co-23: jsonify below is the FIXED handler's generic response shape

log_stream = (
    io.StringIO()
)  # => co-22: captures every log record this example emits, for real inspection below
logger = logging.getLogger(
    "orders_app"
)  # => co-22: a named logger -- filterable independent of other modules
logger.addHandler(
    logging.StreamHandler(log_stream)
)  # => co-22: routes THIS logger's output into log_stream
logger.setLevel(
    logging.ERROR
)  # => co-22: only error-and-above records are captured -- matches production intent

naive_app = Flask(
    __name__
)  # => co-23: the VULNERABLE app -- leaks tracebacks to the CLIENT
naive_app.config["TESTING"] = (
    True  # => co-23: disables Flask's own debugger UI so errorhandler below actually runs
)


@naive_app.route(
    "/divide/<int:n>"
)  # => co-23: a route that can genuinely raise (division by zero)
def naive_divide(
    n: int,
) -> dict[
    str, float
]:  # => co-23: intentionally unguarded -- the bug this route exposes
    """Divide 100 by n with NO error handling of its own -- the errorhandler below catches it."""  # => co-23: doc
    return {
        "result": 100 / n
    }  # => co-23: raises ZeroDivisionError when n == 0, uncaught here


@naive_app.errorhandler(
    Exception
)  # => co-23: catches EVERY uncaught exception in naive_app
def naive_error_handler(
    exc: Exception,
) -> tuple[str, int]:  # => co-23: the VULNERABLE handler, do not copy
    """Return the full traceback text directly to the client -- VULNERABLE, do not copy."""  # => co-23: doc
    return (
        traceback.format_exc(),
        500,
    )  # => co-23: leaks file paths, line numbers, and internal structure to the client


fixed_app = Flask(
    __name__
)  # => co-23: the FIXED app -- generic message to the client, real detail to the log
fixed_app.config["TESTING"] = (
    True  # => co-23: disables Flask's own debugger UI so errorhandler below actually runs
)


@fixed_app.route(
    "/divide/<int:n>"
)  # => co-23: the SAME route shape as naive_divide, same bug potential
def fixed_divide(
    n: int,
) -> dict[
    str, float
]:  # => co-23: identical business logic -- only the ERROR HANDLING differs
    """Divide 100 by n -- identical to naive_divide, the fix lives entirely in the handler below."""  # => co-23: doc
    return {
        "result": 100 / n
    }  # => co-23: raises ZeroDivisionError when n == 0, uncaught here too


@fixed_app.errorhandler(
    Exception
)  # => co-23: catches EVERY uncaught exception in fixed_app
def fixed_error_handler(
    exc: Exception,
) -> tuple[dict[str, str], int]:  # => co-23: the FIXED handler
    """Log the real traceback server-side; return only a generic message to the client -- FIXED."""  # => co-23: doc
    logger.exception(
        "unhandled exception in request"
    )  # => co-22: the REAL traceback, captured in log_stream, never sent to the client
    return {
        "error": "internal server error"
    }, 500  # => co-23: the client gets NOTHING beyond this generic message


if (
    __name__ == "__main__"
):  # => co-23: entry point -- trigger the SAME error against both apps
    print(
        "=== VULNERABLE: client response leaks the full traceback ==="
    )  # => co-23: the leak
    naive_client = (
        naive_app.test_client()
    )  # => co-23: an in-process client -- issues real Flask request/response cycles
    naive_response = naive_client.get(
        "/divide/0"
    )  # => co-23: n=0 triggers a real ZeroDivisionError
    naive_body = naive_response.get_data(
        as_text=True
    )  # => co-23: the ACTUAL response body sent to the client
    print(f"status={naive_response.status_code}")  # => co-23: 500, as expected
    print(
        naive_body[:200] + "..."
    )  # => co-23: file paths and internal structure, visible to the client

    print(
        "\n=== FIXED: client response is generic, real detail goes to the log ==="
    )  # => co-23: re-run against the fix
    fixed_client = (
        fixed_app.test_client()
    )  # => co-23: a SEPARATE in-process client, for the fixed app
    fixed_response = fixed_client.get("/divide/0")  # => co-23: the SAME trigger -- n=0
    fixed_body = (
        fixed_response.get_json()
    )  # => co-23: the ACTUAL response body sent to the client
    print(
        f"status={fixed_response.status_code} body={fixed_body}"
    )  # => co-23: 500, but with NO internal detail

    log_content = (
        log_stream.getvalue()
    )  # => co-22: the REAL captured server-side log, for inspection
    print(
        f"\nserver-side log contains the real traceback: {'ZeroDivisionError' in log_content}"
    )  # => co-22: True

    client_leaks_nothing = "Traceback" not in str(
        fixed_body
    ) and "site-packages" not in str(fixed_body)  # => co-23: mechanical check
    print(
        f"client response leaks NO internal detail: {client_leaks_nothing}"
    )  # => co-23: True -- the fix holds

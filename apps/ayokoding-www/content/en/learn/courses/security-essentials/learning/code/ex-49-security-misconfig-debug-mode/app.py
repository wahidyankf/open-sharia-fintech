"""Example 49: a Flask app whose debug mode is toggled by an env var -- reused for both halves of this example (co-24)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the debug-mode issue itself

import os  # => co-24: reads EX49_DEBUG from the environment -- lets one file serve both runs of this example

from flask import (
    Flask,
)  # => co-24: no extra imports needed -- Flask's own debug flag is the whole example

app = Flask(
    __name__
)  # => co-24: one Flask app, its debug setting controlled entirely by an env var


@app.route(
    "/crash"
)  # => co-24: the ONE route this example's curl calls hit -- always raises for real
def crash() -> (
    str
):  # => co-24: return type is nominal -- this function never actually returns
    raise RuntimeError(
        "unhandled exception -- this is what a real bug in production looks like"
    )  # => co-24: real exc


if (
    __name__ == "__main__"
):  # => co-24: only runs when launched directly, e.g. `EX49_DEBUG=1 python3 app.py &`
    debug_mode = (
        os.environ.get("EX49_DEBUG") == "1"
    )  # => co-24: the REAL misconfiguration toggle for this example
    app.run(
        host="127.0.0.1", port=5049, debug=debug_mode, use_reloader=False
    )  # => co-24: no reloader -- one clean process

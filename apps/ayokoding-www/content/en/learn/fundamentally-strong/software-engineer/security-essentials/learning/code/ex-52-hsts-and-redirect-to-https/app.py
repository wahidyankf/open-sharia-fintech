# learning/code/ex-52-hsts-and-redirect-to-https/app.py
"""Example 52: a real plain-HTTP Flask app redirecting to HTTPS, plus a real HTTPS app sending HSTS (co-18, co-19)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the redirect/HSTS logic itself

import threading  # => co-18: runs the HTTPS listener on a background thread -- the HTTP listener owns the main thread

from flask import (
    Flask,
    redirect,
    request,
)  # => co-18: redirect() builds a real 301 with a Location header

HTTPS_APP = Flask(
    "https_app"
)  # => co-19: a SEPARATE Flask app -- the one real HTTPS listener this example serves
HTTP_APP = Flask(
    "http_app"
)  # => co-18: a SEPARATE Flask app -- the one real plain-HTTP listener this example serves


@HTTPS_APP.after_request  # => co-19: runs on EVERY response this app sends -- the header is never route-specific
def add_hsts_header(
    response,
):  # => co-19: attaches the real, browser-enforced HSTS header to every HTTPS response
    response.headers["Strict-Transport-Security"] = (
        "max-age=31536000; includeSubDomains"  # => co-19: the real header
    )
    return response  # => co-19: a browser that has SEEN this header once will refuse plain-HTTP for a year afterward


@HTTPS_APP.route("/")  # => co-19: the ONE route this example's HTTPS curl call hits
def https_root() -> (
    str
):  # => co-19: a plain string body -- the header (set above) is the point, not the body
    return "served over a real (self-signed) HTTPS connection, HSTS attached"  # => co-19: real, human-readable body


@HTTP_APP.route("/")  # => co-18: the ONE route this example's plain-HTTP curl call hits
def http_root() -> (
    object
):  # => co-18: returns a Flask Response object -- a real 301 redirect
    https_url = f"https://127.0.0.1:5053{request.path}"  # => co-18: points at the REAL HTTPS listener above, not a fake URL
    return redirect(
        https_url, code=301
    )  # => co-18: a real, permanent redirect -- browsers cache 301s across visits


if (
    __name__ == "__main__"
):  # => co-18: only runs when launched directly, e.g. `python3 app.py &`
    https_thread = threading.Thread(  # => co-19: the REAL HTTPS listener, started in the background
        target=HTTPS_APP.run,
        kwargs={
            "host": "127.0.0.1",
            "port": 5053,
            "ssl_context": "adhoc",
            "use_reloader": False,
        },
        daemon=True,  # => co-19: dies automatically when the main (HTTP) thread exits -- no orphaned process
    )
    https_thread.start()  # => co-19: the HTTPS listener is now REALLY accepting connections on port 5053
    HTTP_APP.run(
        host="127.0.0.1", port=5052, use_reloader=False
    )  # => co-18: the plain-HTTP listener, in the main thread

"""Example 23: Flask Hello."""

from flask import Flask  # => a second WSGI framework, contrasted with FastAPI
from flask.wrappers import Response  # => Flask's own response type

# => Flask's own WSGI app object -- served by "flask run", the SAME underlying
# => WSGI protocol Example 7 hand-wrote against, just wrapped in a framework
app = Flask(__name__)  # => __name__ tells Flask where to look for resources


@app.route("/")  # => Flask's routing decorator -- same idea as FastAPI's @app.get
def hello() -> Response:
    """Flask defaults a str return value to a 200 text/html response."""
    # => constructing a Response explicitly (instead of returning a bare str)
    # => lets this route set an EXACT mimetype, matching Example 1's raw
    # => text/plain header rather than Flask's text/html default for a str return
    return app.response_class("hello from flask", mimetype="text/plain")
    # => confirms routing (co-07) works identically across two frameworks

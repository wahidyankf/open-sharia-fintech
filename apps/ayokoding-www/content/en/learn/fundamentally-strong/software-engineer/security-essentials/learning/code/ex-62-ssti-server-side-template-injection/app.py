# learning/code/ex-62-ssti-server-side-template-injection/app.py
"""Example 62: a live Flask app -- user input rendered AS a template executes code, then as DATA it stays inert (co-06, co-25)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the SSTI issue itself

from flask import (
    Flask,
    render_template_string,
    request,
)  # => co-06: render_template_string keeps data OUT of the template
from jinja2 import (
    Template,
)  # => co-06: Jinja2's Template class -- the REAL vulnerable sink this example seeds

app = Flask(
    __name__
)  # => co-06: one Flask app, hosting both the vulnerable and fixed greeting routes
FIXED_TEMPLATE = "Hello, {{ name }}!"  # => co-06: a FIXED, developer-authored template -- never built from input


@app.route(
    "/legacy/greet"
)  # => co-06: VULNERABLE -- user input becomes the TEMPLATE ITSELF, not template data
def legacy_greet() -> str:  # => co-06: real route handler
    name = request.args.get(
        "name", ""
    )  # => co-01: attacker-controlled -- whatever string the caller sends
    # seeded bug: name is concatenated into the TEMPLATE SOURCE, then that source is COMPILED and RUN
    template = Template(
        "Hello, " + name + "!"
    )  # => co-06: the untrusted string becomes real Jinja2 template syntax
    return (
        template.render()
    )  # => co-06: Jinja2 actually EXECUTES whatever expression syntax `name` contains


@app.route(
    "/secure/greet"
)  # => co-06: FIXED -- user input is template CONTEXT DATA, the template itself never changes
def secure_greet() -> str:  # => co-06: real route handler
    name = request.args.get(
        "name", ""
    )  # => co-01: the SAME shape of attacker-controlled input
    return render_template_string(
        FIXED_TEMPLATE, name=name
    )  # => co-06: fix -- name is substituted as a VALUE, not parsed


if (
    __name__ == "__main__"
):  # => co-06: only runs when launched directly, e.g. `python3 app.py &`
    app.run(
        host="127.0.0.1", port=5062
    )  # => co-06: localhost-only, fixed port -- exploit_and_fix.py targets this

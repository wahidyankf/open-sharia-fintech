"""Example 76: Health vs Readiness -- /health never touches the DB, /ready pings it."""
# => co-08: two DIFFERENT questions that sound similar -- "is the process alive" (health) versus
# => "can this instance actually do its job right now" (readiness) -- orchestrators treat them
# => differently: a failed health check usually triggers a RESTART, a failed readiness check
# => just pulls the instance out of the load-balancing rotation until it recovers on its own

import os  # => co-14: reads the TASKS_DB_PATH env var this example's readiness check depends on
import sqlite3  # => co-14: the stdlib DB driver -- readiness pings a REAL connection, never a mock

from fastapi import FastAPI, Response  # => co-08: Response lets a handler override the status code

# => DB_PATH is read from an env var so the SAME code can point at a real file (co-14) or a
# => deliberately unreachable path -- used ONLY to genuinely simulate "the database is down"
# => without faking any response by hand
DB_PATH = os.environ.get("TASKS_DB_PATH", os.path.join(os.path.dirname(__file__), "tasks.db"))  # => co-14: no hardcoded path here at all -- this example's curl run overrides it directly

app = FastAPI()  # => a fresh app -- this example needs no auth, only the health/readiness contrast


def _init_db_if_reachable() -> None:  # => best-effort setup -- readiness below is what actually
    # => PROVES reachability; this function only exists so the "healthy" scenario has a real table
    try:
        conn = sqlite3.connect(DB_PATH)  # => co-14: fails immediately if DB_PATH's directory is gone
        conn.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
        conn.commit()  # => co-14: commits the CREATE TABLE, if the connection above succeeded at all
        conn.close()  # => co-14: closed immediately -- this function runs once, at import time
    except sqlite3.OperationalError:  # => e.g. DB_PATH points at a directory that doesn't exist
        pass  # => intentionally swallowed here -- /ready is the endpoint that surfaces this, not startup


_init_db_if_reachable()  # => co-15: runs once at import time -- may silently no-op, by design above


@app.get("/health")  # => co-08: LIVENESS -- "is the process itself running and responsive at all?"
def health() -> dict[str, str]:
    return {"status": "ok"}  # => co-03: no DB call, no dependency on anything external -- always 200


@app.get("/ready")  # => co-08, co-14: READINESS -- "can this instance actually SERVE a real request?"
def ready(response: Response) -> dict[str, str]:
    try:
        conn = sqlite3.connect(DB_PATH, timeout=1)  # => co-14: a real connection attempt, not a mock --
        # => timeout=1 keeps this check FAST, since a slow readiness probe is nearly as bad as a broken one
        conn.execute("SELECT 1")  # => the cheapest possible real query -- proves the DB genuinely answers
        conn.close()  # => co-14: closed immediately after the probe succeeds
        return {"status": "ready"}  # => co-03: 200 -- the default status FastAPI applies here
    except sqlite3.OperationalError as exc:  # => e.g. "unable to open database file"
        response.status_code = 503  # => co-03: Service Unavailable -- this instance cannot serve
        # => traffic right now; a load balancer reading THIS status is what actually acts on it
        return {"status": "not_ready", "reason": str(exc)}  # => co-11: the real underlying DB error,
        # => surfaced for operator debugging -- never shown to an end user in a production deployment

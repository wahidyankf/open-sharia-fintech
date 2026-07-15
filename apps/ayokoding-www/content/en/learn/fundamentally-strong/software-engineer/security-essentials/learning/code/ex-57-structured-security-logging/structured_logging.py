# learning/code/ex-57-structured-security-logging/structured_logging.py
"""Example 57: real structured JSON security logs -- user/action/outcome, NEVER a password field (co-22)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the logging setup itself

import io  # => co-22: captures the REAL formatted log output in-memory, for this example to inspect
import json  # => co-22: every log line below is REAL JSON -- parsed back with json.loads, not assumed
import logging  # => co-22: the stdlib logging module -- the SAME machinery a real production service would use

CREDENTIALS = {
    "alice": "correct-horse"
}  # => co-22: a real, tiny credential store -- used ONLY to decide outcome


class JsonFormatter(
    logging.Formatter
):  # => co-22: a real Formatter -- controls EXACTLY what ends up on the wire
    def format(
        self, record: logging.LogRecord
    ) -> str:  # => co-22: called once per real log call, by the logging module
        payload = {  # => co-22: the REAL, closed set of fields this formatter ever emits -- nothing else, ever
            "user": getattr(
                record, "user", None
            ),  # => co-22: WHO -- attached via `extra=`, never free-text
            "action": getattr(
                record, "action", None
            ),  # => co-22: WHAT they attempted -- a fixed vocabulary
            "outcome": getattr(
                record, "outcome", None
            ),  # => co-22: the REAL result -- "success" or "failure"
        }  # => co-22: notice: "password" is not, and can never be, a key this formatter reads or emits
        return json.dumps(
            payload
        )  # => co-22: one real, compact JSON object per log line -- machine-queryable


def log_auth_event(
    logger: logging.Logger, user: str, action: str, outcome: str
) -> None:  # => co-22: the ONLY entry point
    # => co-22: this function's signature has NO password parameter at all -- a caller
    # => literally cannot pass a password through this function even by mistake
    logger.info(
        "auth_event", extra={"user": user, "action": action, "outcome": outcome}
    )  # => co-22: the real log call


def authenticate(
    username: str, password: str
) -> bool:  # => co-22: a real, tiny login check -- password stays LOCAL here
    return (
        CREDENTIALS.get(username) == password
    )  # => co-22: password is compared, never logged, never returned


def build_logger() -> tuple[
    logging.Logger, io.StringIO
]:  # => co-22: wires a real logger to an in-memory stream
    stream = (
        io.StringIO()
    )  # => co-22: a real, in-memory sink -- stands in for a real log file/aggregator
    handler = logging.StreamHandler(
        stream
    )  # => co-22: a real stdlib handler, writing to the stream above
    handler.setFormatter(
        JsonFormatter()
    )  # => co-22: EVERY line this handler writes goes through JsonFormatter first
    logger = logging.getLogger(
        "ex57.auth"
    )  # => co-22: a real, named logger -- isolated from Python's root logger
    logger.setLevel(
        logging.INFO
    )  # => co-22: real logs at INFO and above are captured -- DEBUG is dropped
    logger.addHandler(
        handler
    )  # => co-22: wires the REAL handler+formatter pair onto this logger
    logger.propagate = False  # => co-22: keeps this example's captured output limited to exactly this stream
    return (
        logger,
        stream,
    )  # => co-22: both the real logger AND the real stream this example inspects afterward


def main() -> (
    None
):  # => co-22: runs one failed login, one successful login, then queries the REAL captured log
    logger, stream = (
        build_logger()
    )  # => co-22: a real logger wired to a real in-memory stream

    print("=== a real FAILED login attempt (wrong password) ===")  # => labels section
    wrong_password = "not-the-real-password"  # => co-22: a real, deliberately-wrong password -- stays local, never logged
    ok = authenticate(
        "alice", wrong_password
    )  # => co-22: a real authentication check -- returns False here
    log_auth_event(
        logger, user="alice", action="login", outcome="success" if ok else "failure"
    )  # => co-22: real log call
    assert (
        not ok
    )  # => co-22: proves this really was a failed attempt, not a fabricated scenario

    print(
        "=== a real SUCCESSFUL login attempt (correct password) ==="
    )  # => labels section
    ok2 = authenticate(
        "alice", "correct-horse"
    )  # => co-22: a real authentication check -- returns True here
    log_auth_event(
        logger, user="alice", action="login", outcome="success" if ok2 else "failure"
    )  # => co-22: real log call
    assert ok2  # => co-22: proves this really was a successful attempt

    raw_log = (
        stream.getvalue()
    )  # => co-22: the REAL, complete captured log text -- every line this run produced
    print("\n=== raw captured log (real JSON lines) ===")  # => labels section
    print(
        raw_log.strip()
    )  # => co-22: exactly what a real log aggregator would have received, verbatim

    print("\n=== querying the log: every FAILURE outcome ===")  # => labels section
    records = [
        json.loads(line) for line in raw_log.strip().splitlines()
    ]  # => co-22: real JSON parsing, per real line
    failures = [
        r for r in records if r["outcome"] == "failure"
    ]  # => co-22: a REAL, structured query -- not a grep
    print(
        failures
    )  # => co-22: the real, matching record(s) -- directly queryable because the log IS structured JSON
    assert (
        len(failures) == 1 and failures[0]["user"] == "alice"
    )  # => co-22: proves the real failed event is findable

    print(
        "\n=== verifying NO password value ever reached the log ==="
    )  # => labels section
    assert (
        "password" not in raw_log
    )  # => co-22: the literal string "password" never appears as a key OR anywhere else
    assert (
        wrong_password not in raw_log
    )  # => co-22: the REAL wrong password value never appears in the log text
    assert (
        "correct-horse" not in raw_log
    )  # => co-22: the REAL correct password value never appears either
    print(
        "confirmed: zero password-related content in the real captured log"
    )  # => co-22: real, verified conclusion


if (
    __name__ == "__main__"
):  # => co-22: only runs when launched directly, e.g. `python3 structured_logging.py`
    main()  # => co-22: runs both real login attempts, then queries and inspects the real captured log

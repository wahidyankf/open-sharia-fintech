"""Capstone WSGI application."""

import json
from collections.abc import Callable, Iterable

from di import per_request_service
from middleware import errors, logging
from router import Response, resolve


Headers = list[tuple[str, str]]
StartResponse = Callable[[str, Headers], None]


def application(
    environ: dict[str, object], start_response: StartResponse
) -> Iterable[bytes]:
    # => PATH_INFO is the WSGI path seam; no handler receives the raw environ.
    path = str(environ.get("PATH_INFO", "/"))
    if path == "/ranked":
        service = per_request_service()
        handler = lambda: Response(
            200, json.dumps({"items": service.items}).encode("utf-8")
        )
    elif path == "/boom":

        def handler() -> Response:
            raise RuntimeError("contained")
    else:
        handler = resolve(path)
    # => Logging is outside errors, so both successful and failed calls are observed.
    response = logging(errors(handler))()
    reason = (
        "OK"
        if response.status == 200
        else "Not Found"
        if response.status == 404
        else "Internal Server Error"
    )
    start_response(
        f"{response.status} {reason}",
        [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(response.body))),
        ],
    )
    return [response.body]

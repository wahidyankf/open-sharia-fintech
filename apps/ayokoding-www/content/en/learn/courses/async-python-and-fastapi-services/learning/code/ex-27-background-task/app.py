"""Example 27: Deferring Work Past the Response with Background Tasks.

BackgroundTasks runs a side effect AFTER the response is sent, without a full task queue. Run:
uvicorn app:app --port 8000, then: curl localhost:8000/notify  (co-19)
"""

from fastapi import BackgroundTasks, FastAPI  # => BackgroundTasks is the deferred-work verb (co-19)

app = FastAPI()  # => the ASGI application uvicorn serves

events: list[str] = []  # => a stand-in for an external side-effect target (a log, a queue, an email)


def write_event(message: str) -> None:  # => the side effect itself -- NOT awaited on the request path
    events.append(message)  # => runs AFTER the response is already on its way to the client (co-19)


@app.get("/notify")  # => a route that returns fast and defers the slow side effect
def notify(tasks: BackgroundTasks) -> dict[str, str]:  # => BackgroundTasks is injected by FastAPI (co-19)
    tasks.add_task(write_event, "user notified")  # => SCHEDULE the side effect -- does not run it yet
    # => the response returns immediately; write_event runs only AFTER this return is sent (co-19)
    return {"status": "accepted"}  # => the client sees this before write_event has necessarily finished

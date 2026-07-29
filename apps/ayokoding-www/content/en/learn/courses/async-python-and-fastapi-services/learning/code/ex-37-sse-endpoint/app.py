"""Example 37: A Server Sent Events Endpoint.

An SSE endpoint emits a stream of "event:" lines under the text/event-stream media type, which an EventSource
client consumes as discrete events. Run: uvicorn app:app --port 8000, then: curl -N localhost:8000/events  (co-22)
"""

import asyncio  # => asyncio.sleep paces the event stream (co-02)
from collections.abc import AsyncIterator

from fastapi import FastAPI  # => the web framework (co-10)
from fastapi.responses import StreamingResponse  # => streaming response (co-22)

app = FastAPI()  # => the ASGI application uvicorn serves


async def event_stream() -> AsyncIterator[bytes]:  # => yields SSE-formatted event blocks (co-22)
    for i in range(3):  # => three discrete events
        await asyncio.sleep(0.01)  # => pace the stream -- real events arrive on their own schedule (co-02)
        # => an SSE block: a "data:" line followed by a blank line terminator (co-22)
        yield f"data: event {i}\n\n".encode("utf-8")  # => the two newlines END one event


@app.get("/events")  # => an SSE route
async def events() -> StreamingResponse:  # => returns a streaming SSE response
    # => the text/event-stream media type is what makes a browser's EventSource parse it as events (co-22)
    return StreamingResponse(event_stream(), media_type="text/event-stream")  # => incremental SSE stream

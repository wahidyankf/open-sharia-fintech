"""Example 36: Sending Chunks with a Streaming Response.

StreamingResponse yields chunks incrementally instead of buffering the whole body -- first byte out is fast,
peak memory stays flat. Run: uvicorn app:app --port 8000, then: curl -N localhost:8000/stream  (co-22)
"""

from collections.abc import AsyncIterator  # => the shape of the chunk-producing async generator (co-22)

from fastapi import FastAPI  # => the web framework (co-10)
from fastapi.responses import StreamingResponse  # => the streaming-response class (co-22)

app = FastAPI()  # => the ASGI application uvicorn serves


async def generate_chunks(count: int) -> AsyncIterator[bytes]:  # => an async generator yielding BYTE chunks (co-22)
    for i in range(count):  # => produce one chunk per iteration
        yield f"chunk {i}\n".encode("utf-8")  # => each yield flushes one piece to the client immediately (co-22)


@app.get("/stream")  # => a streaming route
async def stream() -> StreamingResponse:  # => returns a StreamingResponse, not a dict
    # => the generator is consumed lazily -- chunks flow as they are produced, not buffered first (co-22)
    return StreamingResponse(generate_chunks(3), media_type="text/plain")  # => incremental, not buffered (co-22)

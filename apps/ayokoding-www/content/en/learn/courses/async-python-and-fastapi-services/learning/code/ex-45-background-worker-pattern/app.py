"""Example 45: A Lifespan Managed Background Worker.

A background task launched in a lifespan handler drains an asyncio.Queue, processing items without blocking
requests. The worker is started at startup and cancelled cleanly at shutdown. Run: uvicorn app:app --port 8000.
(co-19, co-18)
"""

import asyncio  # => asyncio.Queue + create_task (co-19)

from fastapi import FastAPI, Request  # => Request reads app.state (co-18)

app = FastAPI()  # => the ASGI application uvicorn serves


async def worker(queue: asyncio.Queue[str]) -> None:  # => a long-running consumer loop
    while True:  # => runs until cancelled at shutdown
        item = await queue.get()  # => blocks (cooperatively) until an item arrives (co-19)
        try:
            await asyncio.sleep(0.01)  # => simulate processing the item (co-02)
        finally:
            queue.task_done()  # => mark the item processed even if processing raised (co-19)


@app.on_event("startup")  # => LEGACY startup hook -- start the worker once (co-18; see note below)
async def start_worker() -> None:
    queue: asyncio.Queue[str] = asyncio.Queue()  # => the shared queue requests push to
    task = asyncio.create_task(worker(queue))  # => run the worker concurrently with the server (co-19)
    app.state.queue = queue  # => stash the queue so handlers can enqueue
    app.state.worker = task  # => stash the task so shutdown can cancel it


@app.on_event("shutdown")  # => LEGACY shutdown hook -- stop the worker cleanly (co-18)
async def stop_worker() -> None:
    task: asyncio.Task[None] = app.state.worker  # => the task started at startup
    task.cancel()  # => cancel the infinite loop (co-19)
    try:
        await task  # => await cancellation so it actually stops
    except asyncio.CancelledError:  # => the expected outcome of cancel()
        pass


@app.post("/enqueue")  # => a route that hands work to the background worker
async def enqueue(request: Request) -> dict[str, int]:  # => reads the shared queue
    queue: asyncio.Queue[str] = request.app.state.queue  # => the lifespan-created queue
    await queue.put("job")  # => the worker picks this up without blocking the response (co-19)
    return {"queued": queue.qsize()}  # => how many items are pending (co-14)

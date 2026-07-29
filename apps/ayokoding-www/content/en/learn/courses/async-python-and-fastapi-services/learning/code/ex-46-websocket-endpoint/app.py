"""Example 46: A WebSocket Echo Endpoint.

A FastAPI WebSocket route echoes each inbound message back -- a bidirectional, long-lived connection distinct
from the request/response cycle. Run: uvicorn app:app --port 8000, then connect a ws client. (co-22, co-05)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # => WebSocket is the bidirectional verb (co-22)

app = FastAPI()  # => the ASGI application uvicorn serves


@app.websocket("/ws")  # => a WebSocket route -- a long-lived bidirectional connection (co-22)
async def echo(websocket: WebSocket) -> None:  # => the connection object
    await websocket.accept()  # => complete the WS handshake before reading/sending (co-22)
    try:
        while True:  # => the connection stays open across many messages (co-05)
            message = await websocket.receive_text()  # => await the next inbound message (co-05, co-22)
            await websocket.send_text(f"echo: {message}")  # => echo it straight back
    except WebSocketDisconnect:  # => the client closed the connection
        return  # => stop the loop cleanly -- the connection is gone (co-22)

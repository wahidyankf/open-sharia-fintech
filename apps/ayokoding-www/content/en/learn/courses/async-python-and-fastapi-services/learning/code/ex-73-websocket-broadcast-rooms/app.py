"""Example 73: WebSocket Broadcast Rooms.

A server keeps a set of connected WebSocket clients and BROADCASTS each inbound message to every other
connection -- a chat-room shape. Run: uvicorn app:app --port 8000, then connect N ws clients. (co-22, co-05)
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect  # => WebSocket + disconnect handling (co-22)

app = FastAPI()  # => the ASGI application uvicorn serves

_clients: set[WebSocket] = set()  # => the set of currently connected clients (co-22)


@app.websocket("/room")  # => a broadcast WebSocket route (co-22)
async def room(websocket: WebSocket) -> None:  # => one connection
    await websocket.accept()  # => complete the handshake (co-22)
    _clients.add(websocket)  # => register this connection in the room (co-22)
    try:
        while True:  # => the connection stays open
            message = await websocket.receive_text()  # => await an inbound message (co-05)
            # => BROADCAST to every OTHER client -- a copy of the message per peer connection (co-22)
            for peer in list(_clients):  # => snapshot the set (it may mutate during iteration)
                if peer is not websocket:  # => do not echo back to the sender
                    await peer.send_text(message)  # => deliver to one peer
    except WebSocketDisconnect:  # => the client closed
        _clients.discard(websocket)  # => unregister the disconnected client (co-22)

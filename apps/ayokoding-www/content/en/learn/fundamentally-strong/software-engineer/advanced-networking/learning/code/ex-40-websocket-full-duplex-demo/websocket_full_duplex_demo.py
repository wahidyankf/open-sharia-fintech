# learning/code/ex-40-websocket-full-duplex-demo/websocket_full_duplex_demo.py
"""Example 40: WebSockets -- a Minimal Full-Duplex Demo on One Open Connection."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import base64  # => co-17: Sec-WebSocket-Key/Accept are base64-encoded, per RFC 6455
import hashlib  # => co-17: the handshake's accept value is a SHA-1 digest of key+GUID, per RFC 6455 section 1.3
import socket  # => co-17: WebSockets upgrade a PLAIN TCP socket -- no third-party library needed for this minimal demo
import struct  # => co-17: the 2-byte extended-length field in a frame header is packed/unpacked with struct
import threading  # => co-17: runs the server concurrently with the client on one localhost connection

WEBSOCKET_GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"  # => co-17: RFC 6455's own fixed magic GUID, concatenated onto the client's key before hashing
HOST = "127.0.0.1"  # => co-17: loopback -- this demo needs no real network, only a real TCP socket pair


def compute_accept(client_key: str) -> str:  # => co-17: the exact RFC 6455 section 1.3 accept-value algorithm
    """Compute Sec-WebSocket-Accept from a client's Sec-WebSocket-Key, per RFC 6455."""  # => co-17: documents compute_accept's contract -- no runtime output, just sets its __doc__
    digest = hashlib.sha1((client_key + WEBSOCKET_GUID).encode()).digest()  # => co-17: SHA-1 over key+GUID -- the exact bytes the spec requires
    return base64.b64encode(digest).decode()  # => co-17: base64-encode the raw digest -- this is the value both sides must agree on


def recv_until_headers_end(sock: socket.socket) -> bytes:  # => co-17: reads exactly through the blank line ending an HTTP header block
    """Read bytes one at a time until the HTTP header-terminating blank line (\\r\\n\\r\\n) appears."""  # => co-17: documents recv_until_headers_end's contract -- no runtime output, just sets its __doc__
    buffer = b""  # => co-17: accumulates bytes across possibly-separate recv() calls
    while not buffer.endswith(b"\r\n\r\n"):  # => co-17: the HTTP/1.1 header-block terminator, unchanged by the Upgrade
        buffer += sock.recv(1)  # => co-17: one byte at a time is wasteful but simplest for this small demo's fixed-size handshake
    return buffer  # => co-17: returns this computed value to the caller


def make_text_frame(payload: bytes, masked: bool) -> bytes:  # => co-17: builds one RFC 6455 frame -- FIN+text opcode, then payload
    """Build a single unfragmented text-opcode WebSocket frame; client frames MUST be masked, server frames MUST NOT."""  # => co-17: documents make_text_frame's contract -- no runtime output, just sets its __doc__
    header = bytearray()  # => co-17: the frame's leading 2+ bytes, built up field by field below
    header.append(0x81)  # => co-17: FIN=1 (this frame is complete, not fragmented) | opcode=0x1 (text)
    length = len(payload)  # => co-17: this demo's payloads are always small enough to skip the 8-byte extended-length case
    mask_bit = 0x80 if masked else 0x00  # => co-17: the mask bit -- RFC 6455 REQUIRES client-to-server frames to set this
    if length < 126:  # => co-17: RFC 6455's short-length encoding -- length fits directly in the second byte's low 7 bits
        header.append(mask_bit | length)  # => co-17: mask bit plus the literal length, packed into one byte
    else:  # => co-17: RFC 6455's extended 16-bit length encoding, for payloads this demo doesn't otherwise use
        header.append(mask_bit | 126)  # => co-17: 126 is itself the sentinel meaning "read the next 2 bytes as the real length"
        header += struct.pack(">H", length)  # => co-17: the real length, big-endian, exactly as RFC 6455 requires on the wire
    if masked:  # => co-17: only CLIENT frames take this branch -- server-to-client frames must never be masked
        mask_key = b"\x01\x02\x03\x04"  # => co-17: a real client would use 4 CRYPTOGRAPHICALLY RANDOM bytes -- fixed here only for a reproducible demo transcript
        header += mask_key  # => co-17: the mask key travels on the wire immediately after the length field
        payload = bytes(byte ^ mask_key[i % 4] for i, byte in enumerate(payload))  # => co-17: XOR each payload byte with the cycling 4-byte mask key
    return bytes(header) + payload  # => co-17: the complete frame -- header bytes followed by the (possibly masked) payload


def parse_text_frame(data: bytes) -> bytes:  # => co-17: the exact inverse of make_text_frame -- extracts and unmasks the payload
    """Parse one WebSocket frame's bytes and return its (already-unmasked) payload."""  # => co-17: documents parse_text_frame's contract -- no runtime output, just sets its __doc__
    second_byte = data[1]  # => co-17: byte 1 carries the mask bit and the short-length field
    masked = bool(second_byte & 0x80)  # => co-17: True for every client frame this demo parses, False for every server frame
    length = second_byte & 0x7F  # => co-17: the low 7 bits -- this demo's frames never exceed the short-length range
    index = 2  # => co-17: byte offset where the mask key (if present) or payload begins
    if masked:  # => co-17: only frames FROM the client carry a mask key to strip
        mask_key = data[index : index + 4]  # => co-17: the 4-byte key the sender chose for this one frame
        index += 4  # => co-17: advances past the mask key to where the actual payload bytes begin
        payload = bytes(byte ^ mask_key[i % 4] for i, byte in enumerate(data[index : index + length]))  # => co-17: XOR-ing twice with the SAME key recovers the original bytes
    else:  # => co-17: server frames arrive already in plaintext -- no unmasking needed
        payload = data[index : index + length]  # => co-17: the payload bytes, taken directly
    return payload  # => co-17: returns this computed value to the caller


def run_server(listener: socket.socket) -> None:  # => co-17: the SERVER side -- completes the handshake, then reads AND writes on the same connection
    """Accept one client, complete the WebSocket handshake, then demonstrate full-duplex traffic."""  # => co-17: documents run_server's contract -- no runtime output, just sets its __doc__
    conn, _ = listener.accept()  # => co-17: blocks here until the client below connects
    request = recv_until_headers_end(conn)  # => co-17: reads the client's HTTP/1.1 Upgrade request in full
    client_key = None  # => co-17: extracted below from the request's Sec-WebSocket-Key header
    for line in request.split(b"\r\n"):  # => co-17: a minimal header parser -- just enough to find the ONE header this demo needs
        if line.lower().startswith(b"sec-websocket-key:"):  # => co-17: case-insensitive match, since HTTP header names are case-insensitive
            client_key = line.split(b":", 1)[1].strip().decode()  # => co-17: everything after the first colon, whitespace-trimmed
    assert client_key is not None, "the client's Upgrade request must carry a Sec-WebSocket-Key header"  # => co-17
    accept_value = compute_accept(client_key)  # => co-17: the exact value RFC 6455 requires the server to echo back
    response = (  # => co-17: the literal 101 response -- this IS co-17's "upgrade an HTTP connection" step, completed
        "HTTP/1.1 101 Switching Protocols\r\n"  # => co-17: the status line THIS example's syllabus entry (ex-39) is about
        "Upgrade: websocket\r\n"  # => co-17: echoes the client's requested protocol upgrade
        "Connection: Upgrade\r\n"  # => co-17: confirms the connection itself is being repurposed, not just this one response
        f"Sec-WebSocket-Accept: {accept_value}\r\n\r\n"  # => co-17: proves the server understood this IS a WebSocket handshake, not a generic Upgrade
    ).encode()  # => co-17: closes the multi-line construct opened above
    conn.sendall(response)  # => co-17: from THIS point on, both sides speak the WebSocket FRAMING protocol, not HTTP
    conn.sendall(make_text_frame(b"hello from server", masked=False))  # => co-17: the SERVER pushes a message WITHOUT waiting for a client request -- the defining full-duplex behavior
    incoming = parse_text_frame(conn.recv(1024))  # => co-17: the server can ALSO read on the very same connection, no new request needed
    conn.sendall(make_text_frame(b"ack:" + incoming, masked=False))  # => co-17: replies on the SAME connection -- no new handshake, no new socket
    conn.close()  # => co-17: releases this connection's resources on the server side


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-17: the listening socket the server thread accepts on
    listener.bind((HOST, 0))  # => co-17: port 0 -- let the OS pick a free ephemeral port, avoiding hardcoded-port collisions
    listener.listen(1)  # => co-17: one pending connection is all this single-client demo needs
    port = listener.getsockname()[1]  # => co-17: the OS-assigned port, needed by the client below to connect back
    server_thread = threading.Thread(target=run_server, args=(listener,))  # => co-17: runs run_server() concurrently
    server_thread.start()  # => co-17: starts accepting and handshaking in the background

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # => co-17: the CLIENT side -- an ordinary TCP socket until the handshake completes
    client.connect((HOST, port))  # => co-17: a plain TCP connect -- WebSockets ride on top of an ordinary connection, nothing special yet
    client_key = base64.b64encode(b"0123456789012345").decode()  # => co-17: a real client uses 16 RANDOM bytes -- fixed here only for a reproducible demo transcript
    upgrade_request = (  # => co-17: the literal HTTP/1.1 request that STARTS as an ordinary request and ASKS to become a WebSocket
        f"GET / HTTP/1.1\r\nHost: {HOST}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n"  # => co-17: Upgrade + Connection headers together are what signal a protocol-switch request
        f"Sec-WebSocket-Key: {client_key}\r\nSec-WebSocket-Version: 13\r\n\r\n"  # => co-17: version 13 is the version RFC 6455 itself standardized
    ).encode()  # => co-17: closes the multi-line construct opened above
    client.sendall(upgrade_request)  # => co-17: sends the Upgrade request -- Example 39 is this exact request/response pair, captured live
    handshake_response = recv_until_headers_end(client)  # => co-17: reads the server's 101 response in full
    status_line = handshake_response.splitlines()[0].decode()  # => co-17: the first line -- expected to be "HTTP/1.1 101 Switching Protocols"
    print(f"client received: {status_line}")  # => co-17: confirms the handshake succeeded before any frame traffic is attempted
    assert status_line == "HTTP/1.1 101 Switching Protocols", "the handshake must succeed with a literal 101 status"  # => co-17

    pushed_message = parse_text_frame(client.recv(1024))  # => co-17: the server's UNSOLICITED push, read here -- no request preceded it
    print(f"client received unsolicited push: {pushed_message!r}")  # => co-17: this line alone demonstrates co-17's "server can initiate" half of full-duplex
    client.sendall(make_text_frame(b"hi from client", masked=True))  # => co-17: the client ALSO sends, on the same connection, without waiting for another server push
    ack = parse_text_frame(client.recv(1024))  # => co-17: reads the server's reply to the message just sent -- both directions used, one connection
    print(f"client received ack: {ack!r}")  # => co-17: confirms the round trip completed on the SAME connection the push arrived on
    client.close()  # => co-17: releases this connection's resources on the client side
    server_thread.join()  # => co-17: waits for the server thread to finish its handshake/push/reply sequence

    assert pushed_message == b"hello from server", "the server's unsolicited push must arrive intact"  # => co-17
    assert ack == b"ack:hi from client", "the server's reply must echo back the client's own message"  # => co-17
    print("Both directions carried data on one open connection, with no new request issued: True")  # => co-17: reached only if every assert above passed
    # => co-17: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held

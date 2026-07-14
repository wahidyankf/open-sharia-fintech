"""Example 54: UDP Echo Server."""

import socket  # => same stdlib module as TCP -- only the socket TYPE differs (co-08, co-10)

HOST = "127.0.0.1"  # => loopback -- keeps this UDP demo local and deterministic
PORT = 50054  # => co-05: a fresh ephemeral port, unique to this example


def run_server() -> None:  # => a UDP server needs no bind/listen/accept sequence at all
    # SOCK_DGRAM selects UDP: connectionless, message-oriented, no handshake (co-08).
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((HOST, PORT))  # => UDP still binds to claim a local port -- but never listen()s  # fmt: skip
        print(f"listening on {HOST}:{PORT}", flush=True)  # => the signal the client script waits for  # fmt: skip
        # recvfrom (not recv!) returns BOTH the datagram's bytes AND the sender's address --
        # there is no persistent "connection" object like TCP's accept() returns (co-08).
        data, sender_addr = sock.recvfrom(1024)  # => blocks until ONE datagram arrives
        print(f"received {data!r} from {sender_addr}")  # => shows the sender's address, learned here  # fmt: skip
        sock.sendto(data, sender_addr)  # => sendto: no connection needed, just an address  # fmt: skip


if __name__ == "__main__":  # => only runs when invoked directly, not when imported
    run_server()  # => the guard above is WHY this only fires when this file is run as a script

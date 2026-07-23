# learning/code/ex-41-sse-one-way-stream/sse_one_way_stream.py
"""Example 41: Server-Sent Events -- a One-Way text/event-stream, Consumed with curl -N."""  # => co-17: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

import threading  # => co-17: runs the SSE server concurrently so this same script can also act as the client
import time  # => co-17: sleeps between events -- what makes "incrementally, over time" observable rather than instant
from http.server import BaseHTTPRequestHandler, HTTPServer  # => co-17: stdlib-only HTTP server -- no third-party SSE library needed

HOST = "127.0.0.1"  # => co-17: loopback -- this demo needs no real network, only a real long-lived HTTP response
EVENT_COUNT = 4  # => co-17: how many "data:" lines the server streams before closing the response
EVENT_DELAY_SECONDS = 0.2  # => co-17: the gap between events -- long enough to prove they arrive incrementally, not all at once


class SseHandler(BaseHTTPRequestHandler):  # => co-17: one GET handler that streams instead of returning a single fixed body
    def log_message(self, format: str, *args: object) -> None:  # => co-17: silences BaseHTTPRequestHandler's default per-request stderr logging
        """Suppress the base class's default request logging -- keeps this demo's own prints the only output."""  # => co-17: documents log_message's contract -- no runtime output, just sets its __doc__
        pass  # => co-17: intentionally empty -- overriding to do nothing is the standard stdlib way to silence it

    def do_GET(self) -> None:  # => co-17: THE handler co-17's "one long-lived response, server-to-client only" describes
        self.send_response(200)  # => co-17: an SSE response is an ordinary 200 -- no special status code exists for it
        self.send_header("Content-Type", "text/event-stream")  # => co-17: THE header that tells a browser's EventSource (or curl -N) to treat this as SSE, not a normal download
        self.send_header("Cache-Control", "no-cache")  # => co-17: prevents any intermediary from buffering/caching a stream that is meant to arrive incrementally
        self.end_headers()  # => co-17: ends the header block -- everything written after this is the streamed body
        for i in range(EVENT_COUNT):  # => co-17: one loop iteration per event -- nothing here differs from an ordinary write, except the pacing
            event_bytes = f"data: tick {i}\n\n".encode()  # => co-17: the SSE wire format -- a "data:" line, then a BLANK line terminating this one event
            self.wfile.write(event_bytes)  # => co-17: writes directly onto the still-open response socket -- the connection never closes between events
            self.wfile.flush()  # => co-17: WITHOUT an explicit flush, the OS/library buffer could hold this event back, defeating "arrives incrementally"
            time.sleep(EVENT_DELAY_SECONDS)  # => co-17: the pause that makes each event a genuinely separate, later write, not one batched response


if __name__ == "__main__":  # => co-17: entry point -- this block runs only when the file executes directly, not on import
    server = HTTPServer((HOST, 0), SseHandler)  # => co-17: port 0 -- let the OS pick a free ephemeral port, avoiding hardcoded-port collisions
    port = server.server_port  # => co-17: the OS-assigned port, needed by the curl client below to connect back
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)  # => co-17: runs the server's request loop concurrently
    server_thread.start()  # => co-17: starts accepting connections in the background
    time.sleep(0.1)  # => co-17: a brief pause so the server is genuinely listening before the client below connects

    print(f"SSE server listening on http://{HOST}:{port}/")  # => co-17: confirms the server is up before consuming it
    print("Run in a separate terminal to watch events arrive incrementally:")  # => co-17: the standalone client-side command this example's syllabus entry (ex-41) names
    print(f"  curl -N http://{HOST}:{port}/")  # => co-17: -N disables curl's own output buffering, so events print as they arrive, not all at once at the end

    import subprocess  # => co-17: this script also acts as its OWN client -- runs curl itself so the transcript below is genuinely captured

    result = subprocess.run(  # => co-17: invokes curl exactly as a human would from a second terminal
        ["curl", "-s", "-N", f"http://{HOST}:{port}/"],  # => co-17: -s suppresses curl's own progress meter -- only the SSE body itself should print
        capture_output=True,  # => co-17: captures curl's stdout instead of letting it print directly, so this script can inspect it
        text=True,  # => co-17: decodes curl's output as text -- SSE's "data:" lines are always UTF-8 text, per the spec
        timeout=5,  # => co-17: bounds the wait -- this whole stream is expected to finish well under 5 seconds
    )  # => co-17: closes the multi-line construct opened above
    print("\ncaptured curl -N output:")  # => co-17: labels the following block as the actual client-observed transcript
    print(result.stdout)  # => co-17: the raw text curl received -- every "data: tick N" line, each followed by a blank line

    events = [line for line in result.stdout.split("\n\n") if line.strip()]  # => co-17: splits on the blank-line event terminator, dropping any trailing empty chunk
    assert len(events) == EVENT_COUNT, f"expected {EVENT_COUNT} events, got {len(events)}"  # => co-17: confirms every event the server sent actually arrived
    assert events[0] == "data: tick 0", "the FIRST event must be tick 0 -- events arrive in send order"  # => co-17
    assert events[-1] == f"data: tick {EVENT_COUNT - 1}", "the LAST event must be the final tick -- confirms nothing was dropped"  # => co-17
    print(f"All {EVENT_COUNT} events arrived, in order, over one long-lived response: True")  # => co-17: reached only if every assert above passed
    # => co-17: this file is self-verifying: if it exits 0, every assert above passed and the demonstrated claim held
    server.shutdown()  # => co-17: stops the background server loop now that the demo transcript has been captured

#!/usr/bin/env bash
# Example 6: Run the Service in the Foreground. (co-06)
#
# BEFORE wiring up systemd, run the app by hand in the foreground and hit it
# with curl. This cleanly separates "does the app even work" from "does the
# supervision work" -- the single best debugging move when a deploy won't
# respond. Run on the box as the deploy user.

set -euo pipefail  # => fail fast; we want to SEE the error, not paper over it

APP_DIR="/opt/myapp"  # => the home + venv created in Example 5
PORT="8000"  # => an unprivileged local port (1000+); the proxy will front 80/443 later

# --- 1. Put a minimal service in place (reused from backend-essentials) --------
# A tiny stdlib HTTP server that answers "ok" on /health -- the same shape the
# health check (Example 17) and proxy (Example 12) will later target.
cat > "${APP_DIR}/app.py" <<'PY'  # => heredoc writes the service file in place
import http.server  # the standard library's HTTP handler, no framework needed
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):  # answer every GET with a 200 and a short body
        body = b"ok" if self.path == "/health" else b"hello"  # /health is the probe path
        self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass  # keep the foreground output readable
http.server.HTTPServer(("127.0.0.1", 8000), H).serve_forever()  # bind LOOPBACK only (proxy will expose it)
PY

# --- 2. Run it in the FOREGROUND (blocking) -----------------------------------
# This is the literal definition of "hosting": a process serving requests.
# Run in a second terminal so you can curl it while it blocks here.
echo "[run] starting on 127.0.0.1:${PORT} (Ctrl-C to stop) ..."
"${APP_DIR}/venv/bin/python" "${APP_DIR}/app.py"  # => blocks here serving; verify from another shell

# --- 3. Verify (from a SECOND shell, while the above blocks) ------------------
#   curl -s http://127.0.0.1:${PORT}/health   # => expect: ok
#   curl -s http://127.0.0.1:${PORT}/         # => expect: hello
echo "[verify] in another terminal: curl http://127.0.0.1:${PORT}/health"  # => co-06's proof
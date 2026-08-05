"""Generate the essential directives of a systemd service unit."""

unit = """[Service]
Type=simple
ExecStart=/usr/bin/notes-linux-daemon
Restart=on-failure
"""
print(unit)

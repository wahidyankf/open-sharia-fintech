"""Pair a daemon command with systemd's restart policy."""

unit = """[Unit]
Description=Notes daemon

[Service]
ExecStart=/usr/bin/python3 -m notes_linux.daemon
Restart=on-failure
"""
assert "Restart=on-failure" in unit
print(unit)

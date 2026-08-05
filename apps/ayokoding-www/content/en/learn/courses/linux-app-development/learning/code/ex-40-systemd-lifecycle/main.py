"""Describe the systemd actions that manage a changed service."""

commands = [
    "systemctl daemon-reload",
    "systemctl enable --now notes-linux.service",
    "systemctl status notes-linux.service",
]
print("\n".join(commands))

"""Construct a cron schedule for periodic, finite work."""

minute = "*/15"
command = "/usr/local/bin/notes-linux --compact"
print(f"{minute} * * * * {command}")

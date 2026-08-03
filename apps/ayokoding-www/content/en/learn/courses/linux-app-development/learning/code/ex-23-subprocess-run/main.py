"""Run a child process and require success."""

import subprocess

subprocess.run(["printf", "notes-daemon\n"], check=True)

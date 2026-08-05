"""Send application data to a running child process."""

import subprocess

child = subprocess.Popen(
    ["tr", "a-z", "A-Z"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True
)
stdout, _ = child.communicate("notes\\n")
print(stdout.strip(), child.returncode)

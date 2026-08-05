"""Connect one child process's stdout to another's stdin."""

import subprocess

producer = subprocess.Popen(["printf", "note\\n"], stdout=subprocess.PIPE, text=True)
assert producer.stdout is not None
consumer = subprocess.run(
    ["tr", "a-z", "A-Z"],
    stdin=producer.stdout,
    capture_output=True,
    check=True,
    text=True,
)
producer.stdout.close()
producer.wait()
print(consumer.stdout.strip())

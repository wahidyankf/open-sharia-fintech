"""Surface a failed producer in a Unix pipeline."""

import subprocess

producer = subprocess.Popen(
    ["sh", "-c", "printf partial; exit 3"], stdout=subprocess.PIPE
)
assert producer.stdout is not None
consumer = subprocess.run(
    ["cat"], stdin=producer.stdout, capture_output=True, check=True
)
producer.stdout.close()
returncode = producer.wait()
print(consumer.stdout.decode(), returncode)

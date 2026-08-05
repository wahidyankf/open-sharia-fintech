"""Model a bounded daemon work loop."""

import time

running = True
for cycle in range(2):
    if not running:
        break
    print(f"polling cycle {cycle}")
    time.sleep(0.01)
print("daemon loop ended")

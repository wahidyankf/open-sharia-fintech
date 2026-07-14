"""Kata 6 (before): int dict keys silently become str keys after a JSON roundtrip."""

import json

scores: dict[int, str] = {1: "gold", 2: "silver", 3: "bronze"}
restored = json.loads(json.dumps(scores))
print(restored[1])

"""Kata 6 (after): convert the restored keys back to int right after loading."""

import json

scores: dict[int, str] = {1: "gold", 2: "silver", 3: "bronze"}
raw_restored: dict[str, str] = json.loads(json.dumps(scores))
restored: dict[int, str] = {int(key): value for key, value in raw_restored.items()}
print(restored[1])

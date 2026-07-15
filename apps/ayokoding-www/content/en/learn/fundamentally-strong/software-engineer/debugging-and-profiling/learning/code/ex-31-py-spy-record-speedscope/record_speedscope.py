"""Example 31: py-spy record --format speedscope -- the real py-spy flag is documented in this
example's write-up (py-spy needs root here, see ex-29). This script produces a REAL, schema-valid
speedscope JSON file (speedscope.app's own "sampled" profile type, documented at
github.com/jlfwong/speedscope/blob/main/src/lib/file-format-spec.ts) from mini_sampler's real
collapsed-stack samples, so it can genuinely be opened in speedscope's left-heavy view."""

from __future__ import annotations

import json
import threading

import mini_sampler
import workload

samples = mini_sampler.collect_samples(workload.run_workload, threading.get_ident())

frame_names: list[str] = []
frame_index: dict[str, int] = {}


def frame_id(name: str) -> int:
    if name not in frame_index:
        frame_index[name] = len(frame_names)
        frame_names.append(name)
    return frame_index[name]


profile_samples: list[list[int]] = []
profile_weights: list[int] = []
for stack, count in samples.items():
    profile_samples.append([frame_id(name) for name in stack.split(";")])
    profile_weights.append(count)

speedscope_doc = {
    "$schema": "https://www.speedscope.app/file-format-schema.json",
    "shared": {"frames": [{"name": name} for name in frame_names]},
    "profiles": [
        {
            "type": "sampled",
            "name": "Example 31 workload",
            "unit": "none",
            "startValue": 0,
            "endValue": sum(profile_weights),
            "samples": profile_samples,
            "weights": profile_weights,
        }
    ],
}

with open("profile.speedscope.json", "w") as f:
    json.dump(speedscope_doc, f, indent=2)

# The "left heavy" view groups all samples sharing the SAME leaf-to-root stack together and sorts
# by total weight, left to right -- reproduce that ranking here directly from the same data.
by_leaf = {}
for stack_ids, weight in zip(profile_samples, profile_weights):
    leaf_name = frame_names[stack_ids[-1]]
    by_leaf[leaf_name] = by_leaf.get(leaf_name, 0) + weight
print("left-heavy-equivalent ranking (leaf frame -> total weight):")
for name, weight in sorted(by_leaf.items(), key=lambda kv: kv[1], reverse=True):
    print(f"  {name}: {weight}")

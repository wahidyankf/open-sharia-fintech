"""Example 44: recover a task after its attached fixture target disappears."""

# => The first target is unavailable, so a recovery path must attach a replacement.
target = {"id": "target-old", "alive": False}
# => Reattachment selects a new target only when the old target cannot continue.
if not target["alive"]:
    target = {"id": "target-new", "alive": True}
# => The recovered task owns a live, explicitly named replacement target.
assert target == {"id": "target-new", "alive": True}
# => Output is evidence that recovery resumed through reattachment.
print("recovered on target-new")

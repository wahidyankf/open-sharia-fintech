---
description: "Lists the core repository principles this convention implements and respects."
when_to_use: Use when checking which principles justify a rule about subagent orchestration.
---

# Principles Implemented/Respected

This practice implements/respects the following core principles:

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Concurrency caps and polling cadences are deliberate, pre-decided constraints — not reactive responses. The main agent acts from a bounded model rather than spawning speculatively and hoping the API absorbs it.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Stuck detection addresses the root cause (output-token-budget exhaustion during planning, causing silent stall) rather than the symptom (batch never completing). Relaunch restores completion; ignoring a stall compounds delay.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: A single default N (3 background subagents, N+1 total including the main thread) with a clearly-described adjustment path is simpler than an adaptive scheduler — one number to reason about, deliberately set rather than continuously inferred. Three minutes between polls is a single number to remember. Concrete mtime-based stuck detection requires no additional tooling.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The cap, polling interval, and stuck threshold are explicit constants stated in this document. Agents do not infer limits from context; they apply the values here.

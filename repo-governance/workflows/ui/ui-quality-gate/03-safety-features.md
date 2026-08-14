---
title: "Safety Features"
description: The four safeguards that keep the UI quality gate's check-fix loop bounded and reliable.
when_to_use: Use when explaining what protects the UI quality gate from infinite loops or regressions.
---

# Safety Features

- **Max iterations**: Default 7, prevents infinite loops
- **Escalation**: Warning at iteration 5 — suggests manual review
- **Convergence monitoring**: If finding count increases between iterations, pause and flag
- **False-positive persistence**: Findings marked FALSE_POSITIVE are tracked and skipped in subsequent iterations

---
description: "Specifies width constraints for Mermaid flowcharts to keep them readable on narrow viewports."
when_to_use: "Use when a Mermaid flowchart risks becoming too wide to render legibly."
---

# Flowchart Width Constraints

The `rhino-cli md mermaid validate` command enforces a maximum horizontal width of **4 nodes** on any single rank level. "Horizontal" is direction-aware:

- **`graph LR` / `graph RL`**: horizontal = **depth** (number of rank columns, i.e., the longest chain)
- **`graph TD` / `graph TB` / `graph BT`**: horizontal = **span** (maximum nodes at any single rank level)

**Parser notes**: Pipe-labeled edges (`A -->|text| B`) parse correctly as edges. Cyclic diagrams are ranked via DFS back-edge removal before longest-path ranking — a cycle ranks as its underlying chain rather than collapsing every node to rank 0.

**Label length**: the validator enforces **≤ 30 raw characters per line** (each `<br/>`-separated segment measured individually). Note: most renderers visually clip at approximately 20 characters — keep displayed text shorter when possible.

**Automated enforcement**:

```bash
./hippo run --class ephemeral --disk-path . -- \
  apps/rhino-cli/scripts/rhino-bin.sh md mermaid validate
```

Run without flags to perform a repo-wide scan (the Nx target runs with `--exclude apps/rhino-cli/tests/fixtures --exclude plans/done --exclude apps/ayokoding-www/content` plus the standardized noise-skip set) using defaults (MaxWidth=4, unlimited depth). Pass additional `--exclude <prefix>` flags to suppress noise in project-specific runs.

**Gate location**: Runs at **pre-commit (staged `.md` files only)** via the `rhino-cli` pre-commit
hook (lint-staged) via `npx nx run rhino-cli:mermaid:validation`. Does NOT run at pre-push or in a
standalone CI workflow — mermaid validation is folded into lint-staged and `pr-quality-gate.yml`.

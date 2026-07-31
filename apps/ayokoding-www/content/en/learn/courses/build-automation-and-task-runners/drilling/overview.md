---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1.** What does a build rule declare?

<details>
<summary>Answer</summary>

Its target artifact, prerequisite inputs, and the recipe that creates the target.

</details>

**Q2.** When should Make rebuild a file target?

<details>
<summary>Answer</summary>

When the target is missing or one of its prerequisites has a newer modification time.

</details>

## Scenario Judgment

1. A task only names a lint command. Should it need timestamp freshness?
2. A source file changed but its binary was not rebuilt. Which part of the graph should you inspect?
3. Can `make -j` safely run recipes with an undeclared shared output?

<details>
<summary>Answer</summary>

No; inspect the target's prerequisites; and no, because the graph cannot order an undeclared dependency.

</details>

## Hands-On Repetition

1. Run Examples 3, 8, and 11 in fresh course-owned directories.
2. Replace one Make recipe with an automatic variable and verify the output stays identical.
3. Build the capstone, edit its C source, and explain why only one chain rebuilds.

## Automaticity Checklist

- I can distinguish a command runner from a build system.
- I can read target, prerequisite, and recipe from a Make rule.
- I can choose `.PHONY` for an action name.
- I can explain timestamp freshness versus content-hash caching.

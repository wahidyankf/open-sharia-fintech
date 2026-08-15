---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This course assumes [Just Enough Python](../just-enough-python/learning/overview.md) and
[Version Control and Git](../version-control-and-git/learning/overview.md). It reconstructs Git's
content-addressed objects, refs, staging index, and a narrow porcelain surface with safe local
fixtures.

## Scope boundary

This is an instructional implementation of Git ideas, not a replacement Git client. It avoids
network protocols, packed-object performance, worktree edge cases, and mutation of the repository
hosting this course.

## Sources

- [Git internals](https://git-scm.com/book/en/v2/Git-Internals-Plumbing-and-Porcelain)
- [Git object format](https://git-scm.com/docs/gitformat-pack)
- [Python hashlib](https://docs.python.org/3/library/hashlib.html)

All artifacts are original and use isolated temporary stores.

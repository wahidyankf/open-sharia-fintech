---
title: "Artifact: Changelog Entry (Keep a Changelog)"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 45
---

> ex-05 &middot; exercises co-04 &middot; a real `CHANGELOG.md` `[Unreleased]` entry, in Keep a
> Changelog 1.1.0's format.

Keep a Changelog 1.1.0 defines exactly six categories -- `Added`, `Changed`, `Deprecated`,
`Removed`, `Fixed`, `Security` -- and every entry lives under an `## [Unreleased]` heading until the
next tagged release moves it under a dated version heading.

```text
# Changelog

All notable changes to this project are documented in this file, in the format defined by
Keep a Changelog (keepachangelog.com/en/1.1.0/), and this project adheres to Semantic
Versioning (semver.org).

## [Unreleased]

### Added

- `Client.fetch(url, timeout: float = 30.0)` now accepts an optional per-request timeout.

### Fixed

- `parse_date("")` now returns `None` instead of raising `IndexError` on empty input.

## [1.4.0] - 2026-06-02

### Added

- Initial public release of the `Client` HTTP wrapper.
```

**Verify**: both new entries sit under the `## [Unreleased]` heading, and each uses exactly one of
the six Keep a Changelog category headings (`Added` for the new `timeout` parameter, `Fixed` for the
`parse_date` bug) -- matching categories the format actually defines, not an invented one.

**Key takeaway**: a changelog entry is one bullet, filed under one of six fixed categories, under
`Unreleased` until release day moves the whole section under a dated version heading.

**Why It Matters**: a reader deciding whether to upgrade needs "what changed for me," not "what
commits happened." The six fixed categories are the whole value: they force every entry into a
user-facing shape (`Added`/`Fixed`/...) instead of an implementation-facing one -- exactly what the
raw commit log (Example 6) fails to do.

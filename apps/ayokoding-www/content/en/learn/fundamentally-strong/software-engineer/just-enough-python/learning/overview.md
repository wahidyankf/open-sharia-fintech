---
title: "Overview"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Prior topics**: [1 · Just Enough Nvim](../../just-enough-nvim/learning/overview.md) -- you should
  be comfortable opening, editing, and saving files before writing and running Python scripts; the
  [Pass 0 forge capstone](../../capstone-forge-ready/overview.md) is recommended but not
  required.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** installed (`python3 --version`) with
  `venv` and `pip` (both ship with CPython); the `black`, `ruff`, and `pyright` CLIs, installable via
  `pip`. Python is licensed under the **PSF License Version 2**, a Tier-1 free-to-teach license.
- **Assumed knowledge**: basic terminal use. No prior Python is required -- this is the reader's Python
  starting point.

## Why this exists -- the big idea

Pass 1-3 build real software, and they need one default language you can read and run without
ceremony -- this primer makes Python that tool before the topics that lean on it. The one idea worth
keeping if you forget everything else: **Python is executable pseudocode** -- optimize for the reader
first; clarity is the whole point, and speed is bought back later only where measured.

**Cross-cutting big ideas**: `abstraction-and-its-cost` -- Python's high-level built-ins (lists, dicts,
comprehensions) buy readable code and charge runtime overhead you spend deliberately, not by default;
every comprehension in this primer is exactly that trade made visible.
`correctness-vs-pragmatism` -- Python's type hints are optional and unenforced at runtime (Example 84
proves it directly): the language lets you ship first and verify later with a separate tool
(`pyright`), rather than forcing "provably right" before anything runs at all. Both ideas recur
throughout this primer's worked examples, not just in this opening section.

## Install and run your first script

Install Python 3 for your platform (macOS: `brew install python@3.14`; Debian/Ubuntu: your
distribution's current `python3` package, or download from
[python.org/downloads](https://www.python.org/downloads/)), then confirm the version:

```text
$ python3 --version
Python 3.14.3
```

**A note on versions**: this primer's examples were authored and verified against CPython **3.14.3**,
the version installed in the sandbox that produced every captured "Output" block on this site.
[python.org](https://www.python.org/downloads/release/python-3146/) lists **3.14.6** (2026-06-10) as
the current published patch release at authoring time -- any 3.14.x patch behaves identically for
everything this primer teaches (f-strings, type hints, comprehensions, `match`, and the standard
library surface used here are all stable across 3.14 patch releases). `black` **26.5.1** and `ruff`
**0.15.21** are the exact versions this primer's `black`/`ruff` examples (4, 5, 68, 81) were run
against; `pyright` **1.1.411** is the exact version Examples 83-84 were run against. All three are
CVE-clean at authoring time. Strict mode for `pyright` is set via config
(`"typeCheckingMode": "strict"`) or an inline `# pyright: strict` comment -- there is **no** `--strict`
CLI flag.

Every example in this primer is a complete, self-contained `.py` file (or small file set) colocated
under `learning/code/`. The command you will run for almost every one of them is exactly this:

```text
python3 example.py
```

**Exceptions, all deliberate**: Examples 2-5 demonstrate CLI workflows (`-c` inline execution, `venv`
creation, `black`, `ruff`) rather than a single script run; Examples 46, 47, 61-64, 73-75, 81-82 name
their file differently (`mod.py`, `cli.py`, a package under `app/`, and so on) because the filename
itself is part of what the example teaches -- each one states its exact run command in its own **Run**
line.

## How this primer is organized

- **Beginner** (Examples 1-28) -- running Python three ways, virtual environments, `black`/`ruff`,
  the primitive types and type hints, operators, f-strings and string methods, lists, tuples,
  dictionaries, sets, slicing, conditionals, and loops.
- **Intermediate** (Examples 29-60) -- comprehensions and generator expressions, functions (typed
  signatures, defaults, keyword args, `*args`/`**kwargs`, multiple returns), lambdas and closures,
  scope, modules and imports, exceptions, file I/O, JSON, and a first pass at classes.
- **Advanced** (Examples 61-84) -- `argparse` CLIs, multi-module packages, custom exception classes
  and exception chaining, dataclasses, ruff-clean typed signatures, generator functions, custom
  context managers, JSON pipelines, `pytest` unit tests, and static type checking with `pyright`
  (including the one case where `pyright` catches a bug that `python3` itself does not).

Every example cites the concept (`co-NN`) it exercises, and every claim about Python's version,
license, and tooling traces to `python.org`, `docs.python.org`, `peps.python.org`, PyPI, and
`docs.pytest.org`, web-verified 2026-07-12/13 and re-confirmed 2026-07-14.

## Scope: just enough, not comprehensive

This is a **Primer**, not a comprehensive Python reference: it covers exactly the language surface
Pass 1-3's Python-primary topics depend on, and deliberately excludes decorators beyond `@dataclass`,
`async`/`await`, metaclasses, descriptors, the full `typing` module (`Protocol`, `Generic`,
`overload`), packaging/distribution (`pyproject.toml`, wheels, publishing), threading/multiprocessing,
and C-extension interop. Full object-oriented Python is previewed here (Examples 59, 60, 65, 67, 71)
and gets its complete treatment in a later topic. If a Python feature is not exercised by a later
topic in this journey, it is out of scope here on purpose, not by oversight.

---

← Previous: [Pass 0 Capstone · Forge-Ready](../../capstone-forge-ready/overview.md) · Next:
[Beginner Examples](./beginner.md) →

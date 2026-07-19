# 4 · Just Enough Python (Primer, Python)

**prd row**: Pass 1 · Core Foundations · Primer · Python · Learn 104 / Drill 204 · Nvim-ready Yes ·
VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: just enough Python to be productive in the Pass 1–3 Python topics; **not** full mastery.
OOP gets a preview here and full treatment in
[`08-object-oriented-programming-essentials`](./08-object-oriented-programming-essentials.md). Python is
the book's primary language (CPython, PSF-license, Tier-1 DD-21).

## Why this exists · the big idea

- **The problem before the solution**: Pass 1–3 build real software, and they need one default language
  you can read and run without ceremony — this primer makes Python that tool before the topics that lean
  on it.
- **Keep-this-if-you-forget-everything**: Python is executable pseudocode — optimize for the reader
  first; clarity is the whole point, and speed is bought back later only where measured.
- **Big ideas touched**: `abstraction-and-its-cost` — high-level built-ins (lists, dicts, comprehensions)
  buy readable code and charge runtime overhead you spend deliberately, not by default.

## Prerequisites

- **Prior topics**: [topic 1 Just Enough Nvim](./01-just-enough-nvim.md) (to edit/run files); the
  [`capstone-forge-ready`](./03-extending-neovim.md) forge is recommended but not required.
- **Tools & environment**: a macOS/Linux terminal; **Python 3.x** installed (`python3 --version`) with
  `venv` + `pip`; the `black`, `ruff`, and `pyright` CLIs (or installed via `pip`).
- **Assumed knowledge**: basic terminal use; no prior Python required (this is the reader's Python
  starting point).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28). Re-confirm version pins at authoring.

- 2026-07-12 — verified: current CPython stable **3.14.6** (2026-06-10); `python3 -m venv` + `pip`
  workflow unchanged. (python.org)
- 2026-07-12 — verified: `black` **26.5.1**, `ruff` **0.15.21** (2026-07-09) — both current, CVE-clean, CLI
  unchanged. (black.readthedocs.io / astral.sh)
- 2026-07-13 — verified: `pyright` **1.1.411** (2026-06-25) current, no published security advisories;
  installs via `pip install pyright` (a community wrapper by R. Craigie that fetches Microsoft's `pyright`
  npm package). Strict mode is set via config (`typeCheckingMode: strict`) or a `# pyright: strict`
  comment — there is **no** `--strict` CLI flag; a clean run prints `0 errors, 0 warnings, 0 informations`.
  (github.com/microsoft/pyright / PyPI)
- 2026-07-12 — verified: `json` stdlib, f-strings, and `match` are unchanged in 3.14 (PEP 750 t-strings
  are an additive complement to f-strings, not a replacement). (docs.python.org whatsnew/3.14)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to a primary source fetched and read in the retroactive grounding sweep
> (2026-07-12, `web-researcher`). Sources: `docs.python.org`, `python.org`, `peps.python.org`, PyPI,
> `docs.pytest.org`, `docs.astral.sh`, and CPython source. No fabricated sources found.

- **Version + license** — CPython **3.14.6** (2026-06-10) per
  [release page](https://www.python.org/downloads/release/python-3146/) + [PEP 745 schedule](https://peps.python.org/pep-0745/)
  (3.14.7 scheduled 2026-08-04, not yet shipped); license **PSF License Version 2**, verbatim from
  [docs.python.org/license.html](https://docs.python.org/license.html). Fast-moving — re-confirm at authoring.
- **Tooling (co-03)** — `black` **26.5.1** ([PyPI](https://pypi.org/project/black/), CVE-clean:
  [CVE-2026-31900](https://nvd.nist.gov/vuln/detail/CVE-2026-31900) fixed 26.3.0,
  [CVE-2026-32274](https://nvd.nist.gov/vuln/detail/CVE-2026-32274) fixed 26.3.1); `ruff` **0.15.21**
  (2026-07-09, [astral-sh/ruff releases](https://github.com/astral-sh/ruff/releases), no published advisories).
  ruff `F401` unused-import per [rule reference](https://docs.astral.sh/ruff/rules/unused-import/). Pin
  bumped from stale 0.15.20 during grounding.
- **Type checker (co-25)** — `pyright` **1.1.411** (2026-06-25) per
  [microsoft/pyright releases](https://github.com/microsoft/pyright/releases) and
  [PyPI](https://pypi.org/project/pyright/); no advisories
  ([security tab](https://github.com/microsoft/pyright/security/advisories)). Strict mode is enabled by
  config (`"typeCheckingMode": "strict"`) or an inline `# pyright: strict` comment, not a CLI flag, per
  [command-line docs](https://raw.githubusercontent.com/microsoft/pyright/main/docs/command-line.md) +
  [configuration docs](https://raw.githubusercontent.com/microsoft/pyright/main/docs/configuration.md).
  The PyPI `pyright` package is R. Craigie's wrapper around Microsoft's official npm build, not a
  Microsoft-published package.
- **venv (co-02)** — [venv docs](https://docs.python.org/3/library/venv.html): pip installs into the venv
  without explicit instruction; isolated from base environment. Confirmed.
- **Type hints (co-06/13)** — [typing.Optional](https://docs.python.org/3/library/typing.html#typing.Optional)
  ("`Optional[X]` is equivalent to `X | None`"; `X | None` is the modern PEP 604 spelling, both valid for a
  3.14 target); [PEP 585](https://peps.python.org/pep-0585/) confirms built-in `list[int]` generics (3.9+, no
  `typing` import).
- **Collections semantics (co-10/12)** — tuple hashability is conditional per
  [glossary "hashable"](https://docs.python.org/3/glossary.html#term-hashable) ("immutable containers … only
  hashable if their elements are") — co-10 refined accordingly; set `O(1)` average membership per
  [TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity).
- **Worked-example stdlib outputs** — spot-verified against primary docs/source: `math.sqrt(16)`→`4.0`
  ([math docs](https://docs.python.org/3/library/math.html#math.sqrt), "all return values are floats");
  `statistics.mean([1,2,3])`→`2` (int, not float — confirmed against
  [CPython `Lib/statistics.py`](https://raw.githubusercontent.com/python/cpython/main/Lib/statistics.py)
  `_convert` denominator-1 rule); `json.dumps` default `separators=(', ', ': ')`
  ([json docs](https://docs.python.org/3/library/json.html#json.dumps)); `@dataclass` auto-`__repr__`
  ([dataclasses docs](https://docs.python.org/3/library/dataclasses.html)); `argparse` `store_true`
  ([argparse docs](https://docs.python.org/3/library/argparse.html#action)); `pytest.raises` +
  "1 passed" ([pytest docs](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises));
  `Counter.most_common` ([collections docs](https://docs.python.org/3/library/collections.html#collections.Counter.most_common));
  self-documenting `f"{x=}"` (3.8+, [lexical analysis](https://docs.python.org/3/reference/lexical_analysis.html#f-strings)).
- **PEP 750 t-strings** — [PEP 750](https://peps.python.org/pep-0750/) + [What's New 3.14](https://docs.python.org/3/whatsnew/3.14.html):
  additive `string.templatelib`, f-string/`str` behavior untouched. Confirmed.
- **Read more citations** — [PEP 8](https://peps.python.org/pep-0008/) (van Rossum/Warsaw/Coghlan, 2001),
  [PEP 484](https://peps.python.org/pep-0484/) (van Rossum/Lehtosalo/Langa, 2014) — author + year exact;
  _Fluent Python_ 2nd ed. (O'Reilly, 2022) and _Effective Python_ 3rd ed. (Addison-Wesley, 2024, "through
  Python 3.13") confirmed against publisher listings.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 8 (Primer). Each example below cites the co-NN it exercises. -->

- **co-01 · running-python** — CPython runs code three ways: a saved script (`python3 file.py`), an
  inline one-liner (`python3 -c "..."`), and the interactive REPL — no IDE required.
- **co-02 · virtual-environments** — `python3 -m venv` creates an isolated per-project interpreter
  whose `pip` installs dependencies without polluting the system Python.
- **co-03 · formatting-and-linting** — `black` auto-formats to a canonical style and `ruff` lints for
  errors/smells, both run from the CLI as the same gates this repo enforces.
- **co-04 · variables-and-binding** — names are references bound to objects by assignment; Python is
  dynamically typed, so a name can be rebound to a value of any type.
- **co-05 · primitive-types** — `int`, `float`, `str`, `bool`, and `None` are the atomic value types,
  each with literal syntax and its own operators.
- **co-06 · type-hints** — annotations (`x: int`, `def f(a: str) -> bool`, `list[int]`,
  `Optional[T]`) document intent and are verified statically by a type checker (`pyright`, co-25)
  without changing runtime behavior; this book type-annotates **every** Python example (DD-39).
- **co-07 · operators** — arithmetic (`+ - * / // % **`), comparison (`== != < >`), boolean
  (`and`/`or`/`not`), membership (`in`), and identity (`is`) combine values into expressions.
- **co-08 · strings-and-fstrings** — string methods (`.upper()`, `.strip()`, `.split()`) plus
  f-strings (`f"{x}"`, format specs `f"{n:.2f}"`, self-documenting `f"{x=}"`) build and format text.
- **co-09 · lists** — ordered, mutable sequences supporting indexing, `append`/`pop`, and in-place
  reassignment.
- **co-10 · tuples** — ordered, immutable sequences that support unpacking (`a, b = pair`) and are
  hashable when their elements are, making them safe as dict keys.
- **co-11 · dictionaries** — key-value mappings with `[]`/`.get()` access, `.items()` iteration, and
  nested structure for JSON-shaped data.
- **co-12 · sets** — unordered collections of unique elements supporting union/intersection/difference
  and O(1) membership tests.
- **co-13 · slicing** — the `[start:stop:step]` syntax extracts subranges (and reverses via `[::-1]`)
  from any sequence — lists, tuples, strings.
- **co-14 · comprehensions** — list/dict/set comprehensions and generator expressions build
  collections declaratively with an optional filter, replacing explicit build-up loops.
- **co-15 · conditionals** — `if`/`elif`/`else` branch on boolean expressions, with truthiness rules
  (empty collections, `0`, `None`, `""` are falsy).
- **co-16 · loops** — `for`/`while` iterate, with `range`, `enumerate`, `zip`, and `break`/`continue`
  controlling and pairing iteration.
- **co-17 · functions** — `def` defines reusable callables with positional, keyword, and default
  parameters and a `return` value (default `None`).
- **co-18 · variadic-args** — `*args` collects extra positionals into a tuple and `**kwargs` collects
  extra keywords into a dict, enabling flexible signatures.
- **co-19 · lambdas-and-scope** — `lambda` makes small anonymous functions (e.g. sort keys); name
  resolution follows LEGB scope, and closures capture enclosing variables.
- **co-20 · modules-and-imports** — `import`/`from … import` load the standard library and sibling
  modules; the `if __name__ == "__main__":` guard separates library from script entry point.
- **co-21 · exceptions** — `try`/`except`/`else`/`finally` handle errors, `raise` signals them, and the
  built-in exception hierarchy (`ValueError`, `TypeError`, `ZeroDivisionError`, …) classifies them.
- **co-22 · files-and-io** — `open()` inside a `with` block reads/writes text safely, closing the file
  even on error (the context-manager protocol).
- **co-23 · json-serialization** — `json.dumps`/`loads` convert between Python objects and JSON strings,
  and `json.dump`/`load` do the same directly to/from files.
- **co-24 · classes** — a `class` bundles typed attributes and methods with `__init__`; `@dataclass`
  and custom context managers (`__enter__`/`__exit__`) are lightweight variants (full OOP in topic 08).
- **co-25 · static-type-checking** — `pyright` reads the type hints and reports mismatches _without
  running the code_; a clean run ("pyright-clean") is the bar every Python example in this book meets
  (DD-39). Type-checking (`pyright`) and linting (`ruff`) are distinct, complementary passes.

## Worked examples

Colocated under `just-enough-python/learning/code/`; each is a complete file run with `python3 <file>`
(DD-20/DD-30/DD-39) and cites the `co-NN` it exercises. Contiguous `ex-01..ex-84`.

### Beginner

- **ex-01 · hello-script** — a script that prints a fixed greeting — verify `python3 hello.py` prints
  exactly `Hello, world!`. (co-01)
- **ex-02 · run-inline-code** — run a one-liner with `python3 -c "print(6 * 7)"` — verify stdout is
  `42`. (co-01)
- **ex-03 · create-venv-install** — create an isolated env and install a package — verify
  `python3 -m venv .venv && .venv/bin/pip install pytest` exits 0 and `.venv/bin/pip show pytest`
  prints a version. (co-02)
- **ex-04 · format-with-black** — run `black hello.py` on deliberately misformatted code — verify it
  reports `1 file reformatted` and a second run reports `unchanged`. (co-03)
- **ex-05 · lint-with-ruff** — run `ruff check bad.py` on code with an unused import — verify it reports
  an `F401` finding and exits non-zero. (co-03)
- **ex-06 · int-and-float** — assign `count: int = 3` and `ratio: float = 1.5` and print both — verify
  stdout is `3 1.5`. (co-04, co-05, co-06)
- **ex-07 · bool-and-none** — assign `flag: bool = True` and `nothing: None = None` and print — verify
  stdout is `True None`. (co-05, co-06)
- **ex-08 · arithmetic-operators** — print `7 // 2`, `7 % 2`, `2 ** 5` on separate lines — verify stdout
  is `3`, `1`, `32`. (co-07)
- **ex-09 · comparison-operators** — print `3 < 5`, `3 == 3`, `4 != 4` — verify stdout is
  `True True False`. (co-07)
- **ex-10 · boolean-operators** — print `True and False`, `True or False`, `not True` — verify stdout is
  `False True False`. (co-07)
- **ex-11 · fstring-interpolation** — build `f"{name} is {age}"` from typed variables — verify stdout is
  `Ada is 36`. (co-08)
- **ex-12 · fstring-formatting** — format a float with `f"{3.14159:.2f}"` — verify stdout is `3.14`.
  (co-08)
- **ex-13 · string-methods** — call `.upper()`, `.strip()`, and `.split()` on `"  a b c  "` — verify
  the outputs are `A B C`, `a b c`, and `['a', 'b', 'c']`. (co-08)
- **ex-14 · list-basics** — create `nums: list[int] = [1, 2, 3]`, `append(4)`, and print — verify stdout
  is `[1, 2, 3, 4]`. (co-09)
- **ex-15 · list-index-mutate** — set `nums[0] = 9` and print — verify stdout is `[9, 2, 3]`. (co-09)
- **ex-16 · tuple-unpacking** — unpack `x, y = (10, 20)` and print `x, y` — verify stdout is `10 20`.
  (co-10)
- **ex-17 · tuple-immutable** — attempt `t[0] = 9` inside `try` — verify it catches `TypeError` and
  prints `immutable`. (co-10, co-21)
- **ex-18 · dict-basics** — create `ages: dict[str, int] = {"Ada": 36}` and print `ages["Ada"]` —
  verify stdout is `36`. (co-11)
- **ex-19 · dict-iterate-items** — loop `.items()` printing `k=v` per line — verify stdout is `a=1`
  then `b=2`. (co-11, co-16)
- **ex-20 · set-dedup** — build a set from `[1, 1, 2, 3, 3]` and print `len(...)` — verify stdout is
  `3`. (co-12)
- **ex-21 · set-operations** — print sorted union and intersection of `{1,2,3}` and `{2,3,4}` — verify
  stdout is `[1, 2, 3, 4]` then `[2, 3]`. (co-12)
- **ex-22 · slice-list** — print `nums[1:4]` and `nums[::-1]` of `[0,1,2,3,4]` — verify stdout is
  `[1, 2, 3]` then `[4, 3, 2, 1, 0]`. (co-13)
- **ex-23 · slice-string** — print `"python"[0:3]` — verify stdout is `pyt`. (co-13)
- **ex-24 · if-elif-else** — classify an integer's sign — verify it prints `negative`, `zero`, or
  `positive` for inputs `-2`, `0`, `5`. (co-15)
- **ex-25 · truthiness** — test an empty list in an `if` — verify it prints `empty`. (co-15)
- **ex-26 · for-range** — sum `range(1, 6)` and print — verify stdout is `15`. (co-16)
- **ex-27 · while-loop** — count down from 3 to 0 printing each — verify stdout is `3`, `2`, `1`, `0`.
  (co-16)
- **ex-28 · enumerate-zip** — `enumerate(["a","b"])` and `zip([1,2],["x","y"])` printed — verify stdout
  is `0 a` / `1 b` then `1 x` / `2 y`. (co-16)

### Intermediate

- **ex-29 · list-comprehension** — build `[n*n for n in range(5)]` — verify stdout is
  `[0, 1, 4, 9, 16]`. (co-14)
- **ex-30 · comprehension-filter** — build `[n for n in range(6) if n % 2 == 0]` — verify stdout is
  `[0, 2, 4]`. (co-14, co-15)
- **ex-31 · dict-comprehension** — build `{n: n*n for n in range(3)}` — verify stdout is
  `{0: 0, 1: 1, 2: 4}`. (co-14, co-11)
- **ex-32 · set-comprehension** — build `{len(w) for w in ["a","bb","cc"]}` — verify sorted result is
  `[1, 2]`. (co-14, co-12)
- **ex-33 · generator-expression** — print `sum(n*n for n in range(4))` — verify stdout is `14`.
  (co-14)
- **ex-34 · nested-comprehension** — flatten `[[1,2],[3,4]]` with a nested comprehension — verify stdout
  is `[1, 2, 3, 4]`. (co-14)
- **ex-35 · define-typed-function** — define `def add(a: int, b: int) -> int` and print `add(2, 3)` —
  verify stdout is `5`. (co-17, co-06)
- **ex-36 · default-args** — define `greet(name: str = "world")` and call it with and without an
  argument — verify stdout is `Hello, world` then `Hello, Ada`. (co-17)
- **ex-37 · keyword-args** — call a two-parameter function by keyword in reverse order — verify the
  result matches positional order. (co-17)
- **ex-38 · args-kwargs** — define `def f(*args, **kwargs)` printing `len(args)` and `len(kwargs)` —
  verify counts for a sample call are correct. (co-18)
- **ex-39 · return-tuple** — return `(quotient, remainder)` and unpack at the call site — verify
  `divmod`-style output `3 1` for `10, 3`. (co-17, co-10)
- **ex-40 · lambda-sort** — sort `[("b",2),("a",1)]` with `key=lambda p: p[0]` — verify order is
  `[('a', 1), ('b', 2)]`. (co-19)
- **ex-41 · closure-counter** — return a closure that increments captured state — verify successive
  calls print `1`, `2`, `3`. (co-19)
- **ex-42 · scope-global-local** — mutate a module-level counter via the `global` keyword — verify the
  outer value changed to the expected number. (co-19)
- **ex-43 · map-filter** — `list(map(lambda n: n*2, filter(lambda n: n%2==0, range(5))))` — verify
  stdout is `[0, 4, 8]`. (co-19, co-16)
- **ex-44 · import-stdlib-math** — `import math; print(math.sqrt(16))` — verify stdout is `4.0`.
  (co-20)
- **ex-45 · from-import** — `from statistics import mean; print(mean([1, 2, 3]))` — verify stdout is
  `2`. (co-20)
- **ex-46 · name-main-guard** — a module with an `if __name__ == "__main__":` block — verify it prints
  when run with `python3 mod.py` but stays silent when imported. (co-20)
- **ex-47 · custom-module-import** — import a sibling module's typed function and call it — verify the
  imported function's output prints. (co-20)
- **ex-48 · try-except** — catch `ZeroDivisionError` around `1 / 0` — verify it prints `cannot divide`.
  (co-21)
- **ex-49 · try-except-else-finally** — run all four clauses on a success path — verify stdout order is
  `try`, `else`, `finally`. (co-21)
- **ex-50 · raise-valueerror** — `raise ValueError("bad input")` on invalid data — verify the process
  exits non-zero and the message appears in the traceback. (co-21)
- **ex-51 · catch-specific-exceptions** — two `except` branches for `ValueError` vs `KeyError` — verify
  the correct branch runs for each trigger. (co-21)
- **ex-52 · read-text-file** — read `data.txt` with `with open(...)` and print — verify stdout matches
  the file's contents. (co-22)
- **ex-53 · write-text-file** — write two lines then read them back — verify the file contains exactly
  `line1\nline2\n`. (co-22)
- **ex-54 · append-file** — open in `"a"` mode and append a line — verify the file grows by one line
  and keeps prior content. (co-22)
- **ex-55 · json-dumps** — `json.dumps({"a": 1})` — verify stdout is `{"a": 1}`. (co-23)
- **ex-56 · json-loads** — parse `'{"a": 1}'` and print the value of `"a"` — verify stdout is `1`.
  (co-23)
- **ex-57 · json-dump-file** — `json.dump(obj, f)` to `out.json` — verify the file's contents parse
  back to the original object. (co-23, co-22)
- **ex-58 · json-load-file** — `json.load(open("out.json"))` and access a field — verify the expected
  value prints. (co-23, co-22)
- **ex-59 · class-basics** — define `class Point` with `__init__` and a `.move()` method — verify a
  method call prints the updated coordinates. (co-24)
- **ex-60 · class-repr** — add typed attributes and `__repr__` to a class — verify `print(obj)` shows
  `Point(x=1, y=2)`. (co-24, co-06)

### Advanced

- **ex-61 · argparse-cli** — build an `argparse` CLI with one positional `name` argument — verify
  `python3 cli.py Ada` prints `Hello, Ada`. (co-20)
- **ex-62 · argparse-optional-flag** — add a `--upper` store-true flag — verify `python3 cli.py Ada
--upper` prints `HELLO, ADA`. (co-20)
- **ex-63 · argparse-help** — verify `python3 cli.py -h` prints a usage block and exits 0. (co-20)
- **ex-64 · multi-module-package** — a package with `app/__main__.py` importing `app/util.py` — verify
  `python3 -m app` prints the util function's result. (co-20)
- **ex-65 · custom-exception-class** — subclass `Exception` as `InvalidInputError`, raise and catch it
  — verify the handler prints the custom message. (co-21, co-24)
- **ex-66 · reraise-with-context** — `raise RuntimeError(...) from err` — verify the traceback shows
  both the original and chained exception. (co-21)
- **ex-67 · dataclass** — `@dataclass` with typed fields `x: int`, `y: int` — verify auto-generated
  `__repr__` prints `Point(x=1, y=2)`. (co-24, co-06)
- **ex-68 · typed-signatures-ruff-clean** — annotate a function with `Optional[str]` and `list[int]` —
  verify `ruff check` reports no findings and exits 0. (co-06, co-03)
- **ex-69 · comprehension-json-transform** — read a JSON list, uppercase each name via a comprehension,
  write it back — verify the output JSON contains the uppercased names. (co-14, co-23)
- **ex-70 · generator-function-yield** — a `def` using `yield` to produce `0..n` — verify `list(gen(3))`
  is `[0, 1, 2]`. (co-14)
- **ex-71 · context-manager-custom** — a class with `__enter__`/`__exit__` used in a `with` block —
  verify stdout order is `enter`, `body`, `exit`. (co-24, co-22)
- **ex-72 · json-file-roundtrip-pipeline** — read `in.json`, filter records with a comprehension, write
  `out.json` — verify `out.json` holds only the kept records. (co-22, co-23, co-14)
- **ex-73 · exception-exit-code** — let an uncaught exception terminate the script — verify
  `python3 crash.py; echo $?` prints a non-zero code. (co-21, co-01)
- **ex-74 · pytest-unit-test** — write a `pytest` test for a pure typed function — verify `pytest`
  reports `1 passed`. (co-17)
- **ex-75 · pytest-raises** — assert an error with `pytest.raises(ValueError)` — verify the test passes.
  (co-21)
- **ex-76 · nested-dict-access** — navigate a nested dict safely with chained `.get(...)` defaults —
  verify a missing path returns the supplied default. (co-11)
- **ex-77 · sort-dicts-by-key** — sort a list of dicts by a field with `key=lambda d: d["age"]` —
  verify the records print in ascending age order. (co-19, co-11)
- **ex-78 · counter-frequency** — `collections.Counter(words).most_common(1)` — verify it prints the
  most frequent word and its count. (co-20, co-11)
- **ex-79 · enumerate-file-lines** — number lines while reading a file with `enumerate(f, 1)` — verify
  each output line is prefixed by its 1-based number. (co-16, co-22)
- **ex-80 · fstring-debug** — print `f"{value=}"` for `value = 42` — verify stdout is `value=42`.
  (co-08)
- **ex-81 · typed-cli-json-roundtrip** — a fully type-hinted `argparse` CLI that reads JSON, transforms
  it, and writes JSON — verify it round-trips the sample and `ruff check` is clean. (co-06, co-20, co-23)
- **ex-82 · module-docstring-and-main** — a module with a top docstring and `def main() -> None` under
  the name guard — verify running it prints, and `python3 -c "import app; print(app.__doc__)"` shows the
  docstring. (co-20)
- **ex-83 · pyright-clean-pass** — run `pyright` on a fully type-annotated module — verify it reports
  `0 errors`. (co-25, co-06)
- **ex-84 · pyright-catches-type-error** — pass a `str` to a parameter annotated `int` — verify
  `pyright` reports the type error even though `python3` still runs the file (static vs runtime).
  (co-25, co-06)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: write one small (~80–150-line) multi-module Python CLI that reads/validates a JSON input,
  transforms it, writes JSON output, and ships one `pytest` test — exercising collections, functions,
  modules, error handling, and file I/O together.
- **Concepts exercised**: [ ] `argparse` CLI [ ] `venv`+`pip` [ ] collections + comprehensions
  [ ] `try/except` with a raised custom error [ ] `json` read/write with `with` [ ] `if __name__` guard
  [ ] one `pytest` test.
- **Ordered steps**:
  1. `just-enough-python/learning/capstone/code/` — `app/__main__.py` + `app/transform.py` + `tests/`.
     Verify `python3 -m venv .venv && .venv/bin/pip install pytest` succeeds.
  2. Implement `transform.py` (pure function). Verify `.venv/bin/pytest` passes.
  3. Wire `argparse` in `__main__.py` reading a JSON file. Verify `python3 -m app in.json` prints/writes
     the expected JSON and exits 0; a bad file exits non-zero with a clear message.
- **Acceptance criteria**: `pytest` green; the CLI round-trips the sample JSON; invalid input handled
  cleanly; `ruff`/`black` clean.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Fluent Python** — Luciano Ramalho (2nd ed., 2022). Definitive intermediate-to-advanced guide to idiomatic modern Python: data model, type hints, concurrency.
- **Effective Python: 125 Specific Ways to Write Better Python** — Brett Slatkin (3rd ed., 2024). Item-based best-practices, updated through Python 3.13.

**Papers & articles**

- **PEP 8 — Style Guide for Python Code** — van Rossum, Warsaw, Coghlan (2001). Python's official style guide. <https://peps.python.org/pep-0008/>
- **PEP 484 — Type Hints** — van Rossum, Lehtosalo, Langa (2014). Foundational spec of Python's optional static type system. <https://peps.python.org/pep-0484/>

---

← Previous: [3 · Extending Neovim](./03-extending-neovim.md) · Next: [5 · Just Enough Bash](./05-just-enough-bash.md) →

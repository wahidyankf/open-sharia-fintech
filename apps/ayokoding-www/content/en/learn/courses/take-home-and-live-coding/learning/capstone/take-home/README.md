# Task summary take-home

## Brief

Build a small command-line program that reads newline-delimited `owner,count` records and prints a deterministic total for each owner. Reject malformed records with an actionable message. The requested deliverable is deliberately narrow: parsing, validation, aggregation, output, tests, and documentation.

## Run

Requires Python 3.11+; the program itself uses only the standard library.

```bash
printf 'ada,2\nlin,1\nada,3\n' > records.txt
python briefcheck.py records.txt
```

Expected output:

```text
ada: 5
lin: 1
```

## Test

```bash
pytest -q
```

## Decisions and trade-offs

- The input is intentionally a simple `owner,count` line format because that is the stated brief. CSV quoting, streaming very large files, persistence, and a web interface are deferred rather than half-built.
- Parsing and aggregation are separate so malformed input is rejected at the boundary before it can change a total.
- Output is sorted by owner, making command output and tests deterministic.
- The program does not log input records or send telemetry. A real operational tool would need an explicit privacy and retention review before either is added.

## Submission review

- [x] Every brief requirement maps to code or a test.
- [x] Run and test commands work from this directory.
- [x] Happy, empty, malformed, and negative-count paths are covered.
- [x] Deferred work is named rather than quietly omitted.
- [ ] Before a real submission: review the actual brief, `git diff`, dependency list, and time cap.

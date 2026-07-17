"""Example 80: A Functional-Core Log Analyzer With Result Errors and an Applicative Combine."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Result[T]'/'Result[list[LogEntry]]' references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds every immutable record here
from typing import (
    Generic,
    TypeVar,
)  # => Generic/TypeVar make Ok[T] a proper generic container

T = TypeVar("T")  # => the type of the value an Ok wraps


@dataclass(frozen=True)  # => marks Ok immutable, matching the FP style
class Ok(Generic[T]):  # => the class body begins here
    value: T  # => the single field this variant carries


@dataclass(frozen=True)  # => marks Err immutable too
class Err:  # => the class body begins here
    errors: tuple[str, ...]  # => accumulates every malformed line, not just the first


Result = Ok[T] | Err  # => the ADT itself: a Result is EITHER variant


@dataclass(frozen=True)  # => one PARSED, immutable log line
class LogEntry:  # => the class body begins here
    level: str  # => INFO, WARN, or ERROR
    message: str  # => the rest of the line, trimmed


def parse_line(
    line: str, line_number: int
) -> "Result[LogEntry]":  # => PURE CORE: one line -> Result
    parts = line.split(
        ":", 1
    )  # => splits "ERROR:disk full" into ["ERROR", "disk full"]
    if len(parts) != 2 or parts[0] not in (
        "INFO",
        "WARN",
        "ERROR",
    ):  # => the ONLY validity rule
        return Err(
            (f"line {line_number}: malformed entry '{line}'",)
        )  # => a single-error Err, keyed to this line
    return Ok(
        LogEntry(level=parts[0], message=parts[1].strip())
    )  # => success wraps the parsed entry


def parse_all(
    lines: list[str],
) -> "Result[list[LogEntry]]":  # => applicative combine: ALL lines, ALL errors
    entries: list[LogEntry] = []  # => collects every SUCCESSFULLY parsed entry
    errors: list[
        str
    ] = []  # => collects every FAILURE, across every line, not just the first
    for i, line in enumerate(
        lines, start=1
    ):  # => visits EVERY line regardless of earlier failures
        result = parse_line(line, i)  # => delegates to the pure per-line parser
        if isinstance(result, Ok):  # => this particular line parsed cleanly
            entries.append(result.value)  # => a good line contributes an entry
        else:  # => this particular line was malformed
            errors.extend(
                result.errors
            )  # => a bad line contributes its error, parsing CONTINUES
    if errors:  # => at least one line was malformed
        return Err(tuple(errors))  # => reports EVERY malformed line at once
    return Ok(entries)  # => every line parsed cleanly


def count_by_level(
    entries: list[LogEntry],
) -> dict[str, int]:  # => PURE CORE: aggregation step
    counts: dict[str, int] = {}  # => the running per-level total
    for entry in entries:  # => folds every entry into the counts dict
        counts[entry.level] = counts.get(entry.level, 0) + 1  # => accumulates per level
    return counts  # => a fresh dict -- the input list itself is never mutated


def run_shell(
    raw_text: str,
) -> None:  # => IMPERATIVE SHELL: the only function that prints
    lines = raw_text.strip().splitlines()  # => splits the "file contents" into lines
    parsed = parse_all(lines)  # => delegates to the pure, error-accumulating core
    if isinstance(
        parsed, Err
    ):  # => reports every problem found, still just ONE code path
        print(
            f"{len(parsed.errors)} error(s) found:"
        )  # => the shell's own summary line
        for (
            error
        ) in parsed.errors:  # => walks EVERY accumulated error, not just the first
            print(f"  {error}")  # => one printed line per malformed input line
        return  # => stops here -- no report is generated from partially-bad input
    counts = count_by_level(parsed.value)  # => delegates to the pure aggregation core
    for level in sorted(counts):  # => alphabetical report, deterministic output
        print(f"{level}: {counts[level]}")  # => one printed line per log level


good_log = "INFO:started\nWARN:low disk\nERROR:crashed\nINFO:restarted"  # => stands in for a real log file
# => this preview is a smaller version of what the capstone builds end to end
run_shell(good_log)  # => Output: ERROR: 1, then INFO: 2, then WARN: 1

bad_log = "INFO:ok\nnonsense line\nERROR:bad\nanother bad one"  # => two malformed lines mixed in
run_shell(bad_log)  # => Output: 2 error(s) found, both listed

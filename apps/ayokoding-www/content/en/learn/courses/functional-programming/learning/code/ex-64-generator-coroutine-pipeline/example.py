"""Example 64: A Pull Pipeline of yield Stages."""

from typing import Iterator  # => Iterator types every stage in this pipeline


def read_lines(
    text: str,
) -> Iterator[str]:  # => stage 1: text -> a lazy stream of lines
    for line in text.splitlines():  # => walks the raw text one line at a time
        yield line  # => suspends after EACH line, waiting for the next pull


def strip_blank(
    lines: Iterator[str],
) -> Iterator[str]:  # => stage 2: filters out blank lines, lazily
    for line in lines:  # => pulls from stage 1 ONE line at a time
        if line.strip():  # => only forwards lines with real content
            yield line  # => only forwards non-blank lines downstream


def uppercase(
    lines: Iterator[str],
) -> Iterator[str]:  # => stage 3: transforms each surviving line
    for line in lines:  # => pulls from stage 2 ONE line at a time
        yield line.upper()  # => the actual transformation this stage performs


text = "hello\n\nworld\n   \nfp"  # => a raw multi-line string, including blank/whitespace-only lines
pipeline = uppercase(
    strip_blank(read_lines(text))
)  # => THREE stages chained, nothing runs yet

result = list(
    pipeline
)  # => pulling into a list is what finally forces every stage to run

# => each stage suspends independently -- no stage ever buffers its whole output
print(result)  # => Output: ['HELLO', 'WORLD', 'FP']

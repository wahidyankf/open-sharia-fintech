# Caveman Compress 🪨

Caveman Compress is an optional AI-agent utility for shrinking natural-language
memory files while preserving the technical material an agent needs. It is not
part of the OSE product, and a new contributor does not need it to run the
repository.

Use it only when you deliberately want a compact, machine-oriented version of a
prose memory file such as CLAUDE.md, a preference note, or a task list.

## What it does

    source file → compressed working copy
                → <filename>.original.md human-readable backup

The utility keeps code blocks, inline code, URLs, file paths, commands,
headings, lists, tables, dates, and technical names intact. The detailed
contract is in [SKILL.md](./SKILL.md).

## Use it carefully

1. Read [SKILL.md](./SKILL.md) in full before using the utility.
2. Confirm the target is natural-language content, not source code or a
   configuration file.
3. Keep the generated .original.md backup available for human editing.
4. Review the result before relying on it in a future session.

The tool never belongs on secrets, environment files, lockfiles, or executable
source. When uncertain, leave a file unchanged.

## Requirements and invocation

The utility requires Python 3.10 or later. From this skill directory:

    python3 -m scripts <absolute-filepath>

In a compatible agent environment, the intended request form is:

    /caveman:compress <filepath>

## Security

Static scanners can flag the subprocess and file-I/O patterns used by this
utility. Read [SECURITY.md](./SECURITY.md) for its boundaries and rationale
before enabling it in a new environment.

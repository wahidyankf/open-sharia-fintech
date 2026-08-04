---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q.** Why are stdout and stderr separate?  
**A.** stdout is pipeline data; stderr is diagnostic output. A non-zero exit status signals failure.

**Q.** What should a Python SIGTERM handler do?  
**A.** Set a stop flag. The normal loop observes it at a safe point and performs cleanup.

## Applied problems

A child process fails: use `check=True` or inspect its return code, then report a useful diagnostic.

A service must expose local status: use a small Unix-domain socket request/reply protocol.

## Code katas

1. Move a CLI log line from stdout to stderr.
2. Surface a non-zero child-process result.
3. Replace cleanup inside a signal handler with a stop flag.
4. Enforce `0600` on a private config file.
5. Add a `[project.scripts]` console entry point.

## Self-check checklist

- [ ] I can define CLI arguments, streams, and exit statuses.
- [ ] I can use XDG paths, safe modes, temporary files, and atomic replacement.
- [ ] I can handle subprocess failures, pipes, signals, and daemon shutdown.
- [ ] I can package and test a Python CLI and daemon.

## Elaborative interrogation and self-explanation

After each kata, answer these prompts aloud or in writing before checking the solution:

1. Why must the CLI return a non-zero exit code after invalid input, even when it prints a helpful message?
2. Why should a SIGTERM handler set a flag instead of unlinking a socket or writing a file itself?
3. Why is a Unix-domain socket a better fit than TCP for this local daemon status protocol?
4. How does an atomic replacement prevent readers from observing a partly written note?
5. Which behavior belongs in the shared core, and which belongs at the CLI or daemon boundary?

For each answer, name the observable contract (stream, exit code, file mode, signal, or socket reply), then explain the failure that the contract prevents.

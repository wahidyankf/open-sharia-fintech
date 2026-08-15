---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
prerequisites: ["just-enough-c", "just-enough-bash"]
---

## Linux-only boundary

This is a **Linux kernel interface** course. Run it on native Linux, a Linux VM, container with the needed permissions, or WSL2. Its `/proc` layouts, `strace`, POSIX/Linux syscalls, `signalfd`, mount namespaces, and scheduler observations are not Windows APIs. The paired [Windows OS](/en/learn/courses/windows-os/overview) course covers Windows process handles, Win32/NT tooling, and their observability model; do not translate these examples by substituting PowerShell commands.

## Prerequisites

- [Just Enough C](/en/learn/courses/just-enough-c/overview): pointers, `struct`, compilation, errno.
- [Just Enough Bash](/en/learn/courses/just-enough-bash/overview): commands, redirection, jobs, and exit statuses.
- Linux with `gcc` or `clang`, `make`, `ps`, `/proc`, and `strace` installed.

## Big idea

The kernel gives isolated processes a small syscall interface for CPU time, memory, files, and communication. Learn the interface by running a compact C experiment, observing it, then changing one condition.

The course has 78 contiguous, runnable, annotated C experiments. From an example directory use:

```sh
cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example
```

For syscall observations, use `strace -f ./example`; for live process evidence, use the PID printed by the program with `ps -o pid,ppid,stat,ni,cmd -p "$PID"` and `cat /proc/$PID/status`.

## The 30 concepts

1. kernel vs user mode; 2. syscalls; 3. `strace`; 4. process model; 5. `fork`; 6. `exec`; 7. `wait`; 8. fork-exec-wait; 9. signals; 10. signal delivery; 11. process states; 12. virtual memory; 13. paging; 14. address-space layout; 15. `mmap`; 16. heap break; 17. file descriptors; 18. inodes; 19. VFS; 20. permissions; 21. mounts; 22. pipes; 23. shared memory; 24. Unix sockets; 25. scheduling; 26. threads vs processes; 27. `nice`; 28. proc filesystem; 29. process tools; 30. portable OS theory.

## Route

- Beginner (01–26): syscall boundary, process control, signals, `/proc`, descriptors, and filesystems.
- Intermediate (27–54): pipes, signal coordination, virtual memory, shared memory, sockets, and scheduling evidence.
- Advanced (55–78): compose the primitives, expose failure modes, and audit the result.
- Capstone: a supervised process tour with `fork`, `exec`, `wait`, signals, pipe, shared `mmap`, `/proc`, `ps`, and `strace` proof.

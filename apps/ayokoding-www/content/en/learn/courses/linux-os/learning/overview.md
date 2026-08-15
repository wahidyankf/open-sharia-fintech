---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Run safely and observe honestly

These examples are intentionally Linux-only. Use a disposable directory and never point permission, mount-namespace, or daemon experiments at production paths. Some observations vary with kernel version, distribution, permissions, CPU load, and container policy. Record the command and the output you actually see; an absent tool is a setup issue, not evidence that a syscall did not occur.

Every code example is annotated at the source and paired with a verification command in its section. Compile C files with `cc -std=c11 -Wall -Wextra -Werror main.c -o example`. A few examples require `-pthread` or `-lrt`; their source comment says so.

## Concepts

- **co-01 · Kernel and user mode** — unprivileged code asks the privileged kernel; isolation is enforced at this boundary.
- **co-02 · System calls** — a syscall transfers a request and returns a result or errno.
- **co-03 · Tracing** — strace reports the syscall boundary, not every line of C.
- **co-04 · Process model** — a PID and PPID place a process in a tree.
- **co-05 · fork** — fork copies a process execution context into parent and child paths.
- **co-06 · exec** — exec replaces a process image while retaining its identity.
- **co-07 · wait** — waitpid collects a terminated child and its status.
- **co-08 · Shell launch** — shells compose fork, exec, and wait.
- **co-09 · Signals** — signals asynchronously change process control flow.
- **co-10 · Signal delivery** — kill selects a target process or group.
- **co-11 · Process states** — running, sleeping, stopped, and zombie states describe lifecycle.
- **co-12 · Virtual memory** — each process has private virtual addresses.
- **co-13 · Paging** — first access can materialize a page on demand.
- **co-14 · Address-space layout** — text, data, heap, mappings, and stack occupy separate regions.
- **co-15 · mmap** — mmap installs a file-backed or anonymous address range.
- **co-16 · Heap break** — the program break is one allocator backing mechanism.
- **co-17 · File descriptors** — integer handles name open files and streams.
- **co-18 · Inodes** — names resolve to metadata objects that may have many links.
- **co-19 · VFS** — the same read/write API spans many filesystem implementations.
- **co-20 · Permissions** — mode bits and ownership constrain access.
- **co-21 · Mounts** — a filesystem becomes visible at a directory mount point.
- **co-22 · Pipes** — a pipe is a one-way kernel byte stream.
- **co-23 · Shared memory** — a shared mapping gives processes common bytes.
- **co-24 · Unix sockets** — Unix sockets provide bidirectional local IPC.
- **co-25 · Scheduling** — Linux decides which runnable task gets CPU time.
- **co-26 · Threads and processes** — threads share an address space; processes do not.
- **co-27 · Nice priority** — nice is a scheduling weight hint, not a deadline.
- **co-28 · proc filesystem** — /proc presents live kernel and process state as files.
- **co-29 · Process tools** — ps and top summarize process state for humans.
- **co-30 · OS theory** — process, memory, filesystem, and IPC abstractions recur across OSes.

## Accessible mechanism maps

Each Mermaid figure has a text equivalent immediately above it. The repeated three-node shape is intentional: it teaches that a user-space request crosses into the kernel and returns an observable result.

### Diagram 01: Kernel and user mode

Text equivalent: unprivileged code asks the privileged kernel; isolation is enforced at this boundary.

```mermaid
flowchart LR
  U[User program] -->|kernel and user mode| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 02: System calls

Text equivalent: a syscall transfers a request and returns a result or errno.

```mermaid
flowchart LR
  U[User program] -->|system calls| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 03: Tracing

Text equivalent: strace reports the syscall boundary, not every line of C.

```mermaid
flowchart LR
  U[User program] -->|tracing| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 04: Process model

Text equivalent: a PID and PPID place a process in a tree.

```mermaid
flowchart LR
  U[User program] -->|process model| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 05: fork

Text equivalent: fork copies a process execution context into parent and child paths.

```mermaid
flowchart LR
  U[User program] -->|fork| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 06: exec

Text equivalent: exec replaces a process image while retaining its identity.

```mermaid
flowchart LR
  U[User program] -->|exec| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 07: wait

Text equivalent: waitpid collects a terminated child and its status.

```mermaid
flowchart LR
  U[User program] -->|wait| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 08: Shell launch

Text equivalent: shells compose fork, exec, and wait.

```mermaid
flowchart LR
  U[User program] -->|shell launch| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 09: Signals

Text equivalent: signals asynchronously change process control flow.

```mermaid
flowchart LR
  U[User program] -->|signals| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 10: Signal delivery

Text equivalent: kill selects a target process or group.

```mermaid
flowchart LR
  U[User program] -->|signal delivery| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 11: Process states

Text equivalent: running, sleeping, stopped, and zombie states describe lifecycle.

```mermaid
flowchart LR
  U[User program] -->|process states| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 12: Virtual memory

Text equivalent: each process has private virtual addresses.

```mermaid
flowchart LR
  U[User program] -->|virtual memory| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 13: Paging

Text equivalent: first access can materialize a page on demand.

```mermaid
flowchart LR
  U[User program] -->|paging| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 14: Address-space layout

Text equivalent: text, data, heap, mappings, and stack occupy separate regions.

```mermaid
flowchart LR
  U[User program] -->|address-space layout| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 15: mmap

Text equivalent: mmap installs a file-backed or anonymous address range.

```mermaid
flowchart LR
  U[User program] -->|mmap| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 16: Heap break

Text equivalent: the program break is one allocator backing mechanism.

```mermaid
flowchart LR
  U[User program] -->|heap break| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 17: File descriptors

Text equivalent: integer handles name open files and streams.

```mermaid
flowchart LR
  U[User program] -->|file descriptors| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 18: Inodes

Text equivalent: names resolve to metadata objects that may have many links.

```mermaid
flowchart LR
  U[User program] -->|inodes| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 19: VFS

Text equivalent: the same read/write API spans many filesystem implementations.

```mermaid
flowchart LR
  U[User program] -->|vfs| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 20: Permissions

Text equivalent: mode bits and ownership constrain access.

```mermaid
flowchart LR
  U[User program] -->|permissions| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 21: Mounts

Text equivalent: a filesystem becomes visible at a directory mount point.

```mermaid
flowchart LR
  U[User program] -->|mounts| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 22: Pipes

Text equivalent: a pipe is a one-way kernel byte stream.

```mermaid
flowchart LR
  U[User program] -->|pipes| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 23: Shared memory

Text equivalent: a shared mapping gives processes common bytes.

```mermaid
flowchart LR
  U[User program] -->|shared memory| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 24: Unix sockets

Text equivalent: Unix sockets provide bidirectional local IPC.

```mermaid
flowchart LR
  U[User program] -->|unix sockets| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 25: Scheduling

Text equivalent: Linux decides which runnable task gets CPU time.

```mermaid
flowchart LR
  U[User program] -->|scheduling| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 26: Threads and processes

Text equivalent: threads share an address space; processes do not.

```mermaid
flowchart LR
  U[User program] -->|threads and processes| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 27: Nice priority

Text equivalent: nice is a scheduling weight hint, not a deadline.

```mermaid
flowchart LR
  U[User program] -->|nice priority| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 28: proc filesystem

Text equivalent: /proc presents live kernel and process state as files.

```mermaid
flowchart LR
  U[User program] -->|proc filesystem| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 29: Process tools

Text equivalent: ps and top summarize process state for humans.

```mermaid
flowchart LR
  U[User program] -->|process tools| K[Linux kernel]
  K --> O[Observable result]
```

### Diagram 30: OS theory

Text equivalent: process, memory, filesystem, and IPC abstractions recur across OSes.

```mermaid
flowchart LR
  U[User program] -->|os theory| K[Linux kernel]
  K --> O[Observable result]
```

---

← Previous: [Course overview](../overview.md) · Next: [Beginner examples](./beginner.md) →

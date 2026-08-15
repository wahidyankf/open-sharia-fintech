---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

## Intermediate: examples 27–54

Run each experiment on Linux. Each source begins with an annotation naming the system contract it probes. The listed observation is a starting point; compare it with your own machine's output.

### Example 27: Basic pipe

**Concept:** co-22. **Why:** pipe basic makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-27-pipe-basic`.

**Observe:** Use `strace -f -e trace=pipe,read,write ./example` and verify unused ends close.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-27-pipe-basic/main.c)

### Example 28: Redirect with dup2

**Concept:** co-22. **Why:** pipe dup2 makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-28-pipe-dup2`.

**Observe:** Use `strace -f -e trace=pipe,read,write ./example` and verify unused ends close.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-28-pipe-dup2/main.c)

### Example 29: Emulate a shell pipeline

**Concept:** co-08. **Why:** pipe shell emulate makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-29-pipe-shell-emulate`.

**Observe:** Use `strace -f -e trace=pipe,read,write ./example` and verify unused ends close.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-29-pipe-shell-emulate/main.c)

### Example 30: Signal between processes

**Concept:** co-10. **Why:** signal between processes makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-30-signal-between-processes`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-30-signal-between-processes/main.c)

### Example 31: Reliable sigaction

**Concept:** co-09. **Why:** sigaction makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-31-sigaction`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-31-sigaction/main.c)

### Example 32: Block a signal

**Concept:** co-09. **Why:** signal mask makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-32-signal-mask`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-32-signal-mask/main.c)

### Example 33: Anonymous mmap

**Concept:** co-15. **Why:** mmap anon makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-33-mmap-anon`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-33-mmap-anon/main.c)

### Example 34: File mapping

**Concept:** co-15. **Why:** mmap file makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-34-mmap-file`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-34-mmap-file/main.c)

### Example 35: Shared mmap

**Concept:** co-23. **Why:** mmap shared makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-35-mmap-shared`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-35-mmap-shared/main.c)

### Example 36: Create POSIX shared memory

**Concept:** co-23. **Why:** shm open makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-36-shm-open`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-36-shm-open/main.c)

### Example 37: Share data with shm

**Concept:** co-23. **Why:** shm ipc makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-37-shm-ipc`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-37-shm-ipc/main.c)

### Example 38: Unix socket

**Concept:** co-24. **Why:** unix socket makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-38-unix-socket`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-38-unix-socket/main.c)

### Example 39: Socket pair

**Concept:** co-24. **Why:** socketpair makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-39-socketpair`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-39-socketpair/main.c)

### Example 40: One VFS API

**Concept:** co-19. **Why:** vfs same api makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-40-vfs-same-api`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-40-vfs-same-api/main.c)

### Example 41: Inspect heap break

**Concept:** co-16. **Why:** heap brk makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-41-heap-brk`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-41-heap-brk/main.c)

### Example 42: Trace allocation

**Concept:** co-16. **Why:** malloc strace makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-42-malloc-strace`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-42-malloc-strace/main.c)

### Example 43: Address-space segments

**Concept:** co-14. **Why:** address space segments makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-43-address-space-segments`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-43-address-space-segments/main.c)

### Example 44: Demand page fault

**Concept:** co-13. **Why:** page fault makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-44-page-fault`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-44-page-fault/main.c)

### Example 45: Trace open/read/close

**Concept:** co-03. **Why:** strace openfile makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-45-strace-openfile`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-45-strace-openfile/main.c)

### Example 46: Count syscalls

**Concept:** co-03. **Why:** strace count makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-46-strace-count`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-46-strace-count/main.c)

### Example 47: Draw a process tree

**Concept:** co-29. **Why:** ps tree makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-47-ps-tree`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-47-ps-tree/main.c)

### Example 48: Observe nice

**Concept:** co-27. **Why:** nice priority makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-48-nice-priority`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-48-nice-priority/main.c)

### Example 49: Thread versus process

**Concept:** co-26. **Why:** thread vs process makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-49-thread-vs-process`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-49-thread-vs-process/main.c)

### Example 50: Count context switches

**Concept:** co-25. **Why:** context switch count makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-50-context-switch-count`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-50-context-switch-count/main.c)

### Example 51: Reap a zombie

**Concept:** co-11. **Why:** zombie reap makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-51-zombie-reap`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-51-zombie-reap/main.c)

### Example 52: Observe reparenting

**Concept:** co-04. **Why:** orphan reparent makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-52-orphan-reparent`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-52-orphan-reparent/main.c)

### Example 53: Read proc cmdline

**Concept:** co-28. **Why:** proc cmdline makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-53-proc-cmdline`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-53-proc-cmdline/main.c)

### Example 54: Read signals as descriptors

**Concept:** co-09. **Why:** signalfd makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-54-signalfd`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-54-signalfd/main.c)

---

← Previous: [Learning overview](./overview.md) · Next: [Advanced](./advanced.md) →

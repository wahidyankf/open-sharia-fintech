---
title: "Advanced Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

## Advanced: examples 55–78

Run each experiment on Linux. Each source begins with an annotation naming the system contract it probes. The listed observation is a starting point; compare it with your own machine's output.

### Example 55: Mini shell

**Concept:** co-08. **Why:** shell mini makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-55-shell-mini`.

**Observe:** Confirm that the post-exec output has the same PID identity but a replaced program image.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-55-shell-mini/main.c)

### Example 56: Shell pipeline

**Concept:** co-22. **Why:** shell pipe makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-56-shell-pipe`.

**Observe:** Confirm that the post-exec output has the same PID identity but a replaced program image.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-56-shell-pipe/main.c)

### Example 57: Shell signal policy

**Concept:** co-09. **Why:** shell signal makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-57-shell-signal`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-57-shell-signal/main.c)

### Example 58: Producer/consumer shared memory

**Concept:** co-23. **Why:** producer consumer shm makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-58-producer-consumer-shm`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-58-producer-consumer-shm/main.c)

### Example 59: Map a large file

**Concept:** co-15. **Why:** mmap large file makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-59-mmap-large-file`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-59-mmap-large-file/main.c)

### Example 60: Copy on write

**Concept:** co-13. **Why:** copy on write makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-60-copy-on-write`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-60-copy-on-write/main.c)

### Example 61: Find a descriptor leak

**Concept:** co-05. **Why:** fd leak detect makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-61-fd-leak-detect`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-61-fd-leak-detect/main.c)

### Example 62: Trace a socket

**Concept:** co-17. **Why:** strace network makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-62-strace-network`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-62-strace-network/main.c)

### Example 63: Signal-safe race handling

**Concept:** co-24. **Why:** signal race makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-63-signal-race`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-63-signal-race/main.c)

### Example 64: Nonblocking waitpid

**Concept:** co-09. **Why:** waitpid nonblock makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-64-waitpid-nonblock`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-64-waitpid-nonblock/main.c)

### Example 65: Signal a process group

**Concept:** co-07. **Why:** process group makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-65-process-group`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-65-process-group/main.c)

### Example 66: Double-fork detachment

**Concept:** co-10. **Why:** daemon double fork makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-66-daemon-double-fork`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-66-daemon-double-fork/main.c)

### Example 67: Mount namespace boundary

**Concept:** co-08. **Why:** mount namespace makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-67-mount-namespace`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-67-mount-namespace/main.c)

### Example 68: Compare proc and disk VFS

**Concept:** co-21. **Why:** vfs proc vs disk makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-68-vfs-proc-vs-disk`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-68-vfs-proc-vs-disk/main.c)

### Example 69: Observe scheduler time slices

**Concept:** co-19. **Why:** scheduler observe makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-69-scheduler-observe`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-69-scheduler-observe/main.c)

### Example 70: Inspect threads in top

**Concept:** co-25. **Why:** top threads makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-70-top-threads`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-70-top-threads/main.c)

### Example 71: Shared mmap counter

**Concept:** co-26. **Why:** mmap shared counter makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-71-mmap-shared-counter`.

**Observe:** While it runs, inspect `/proc/$PID/maps`; map addresses vary, permissions and mapping type are the evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-71-mmap-shared-counter/main.c)

### Example 72: Pipe closure prevents deadlock

**Concept:** co-23. **Why:** pipe deadlock makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-72-pipe-deadlock`.

**Observe:** Use `strace -f -e trace=pipe,read,write ./example` and verify unused ends close.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-72-pipe-deadlock/main.c)

### Example 73: Hard-link inode

**Concept:** co-22. **Why:** inode hardlink makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-73-inode-hardlink`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-73-inode-hardlink/main.c)

### Example 74: Observe EACCES

**Concept:** co-18. **Why:** permission denied makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-74-permission-denied`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-74-permission-denied/main.c)

### Example 75: Trace signal delivery

**Concept:** co-20. **Why:** strace signal makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-75-strace-signal`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-75-strace-signal/main.c)

### Example 76: Full IPC slice

**Concept:** co-09. **Why:** full ipc slice makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-76-full-ipc-slice`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-76-full-ipc-slice/main.c)

### Example 77: Observe the IPC slice

**Concept:** co-23. **Why:** integration observe slice makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-77-integration-observe-slice`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-77-integration-observe-slice/main.c)

### Example 78: Capstone process tour

**Concept:** co-28. **Why:** capstone process tour makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-78-capstone-process-tour`.

**Observe:** Run the capstone proof sequence and account for process, signal, pipe, mapping, and reaping evidence.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-78-capstone-process-tour/main.c)

---

← Previous: [Learning overview](./overview.md) · Next: [Capstone](./capstone.md) →

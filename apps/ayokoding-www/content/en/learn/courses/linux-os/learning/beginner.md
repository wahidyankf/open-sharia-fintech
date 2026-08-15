---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

## Beginner: examples 1–26

Run each experiment on Linux. Each source begins with an annotation naming the system contract it probes. The listed observation is a starting point; compare it with your own machine's output.

### Example 1: Hello with write

**Concept:** co-02. **Why:** hello syscall makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-01-hello-syscall`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-01-hello-syscall/main.c)

### Example 2: Trace hello

**Concept:** co-03. **Why:** strace hello makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-02-strace-hello`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-02-strace-hello/main.c)

### Example 3: Print a PID

**Concept:** co-04. **Why:** getpid makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-03-getpid`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-03-getpid/main.c)

### Example 4: Fork a child

**Concept:** co-05. **Why:** fork basic makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-04-fork-basic`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-04-fork-basic/main.c)

### Example 5: Fork return values

**Concept:** co-05. **Why:** fork return makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-05-fork-return`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-05-fork-return/main.c)

### Example 6: Replace with exec

**Concept:** co-06. **Why:** exec basic makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-06-exec-basic`.

**Observe:** Confirm that the post-exec output has the same PID identity but a replaced program image.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-06-exec-basic/main.c)

### Example 7: Fork then exec ls

**Concept:** co-06. **Why:** exec ls makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-07-exec-ls`.

**Observe:** Confirm that the post-exec output has the same PID identity but a replaced program image.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-07-exec-ls/main.c)

### Example 8: Reap a child

**Concept:** co-07. **Why:** wait child makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-08-wait-child`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-08-wait-child/main.c)

### Example 9: Fork, exec, wait

**Concept:** co-08. **Why:** fork exec wait makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-09-fork-exec-wait`.

**Observe:** Confirm that the post-exec output has the same PID identity but a replaced program image.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-09-fork-exec-wait/main.c)

### Example 10: Read an exit status

**Concept:** co-07. **Why:** exit status makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-10-exit-status`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-10-exit-status/main.c)

### Example 11: Observe a zombie

**Concept:** co-11. **Why:** zombie makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-11-zombie`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-11-zombie/main.c)

### Example 12: Catch SIGINT

**Concept:** co-09. **Why:** signal handler makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-12-signal-handler`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-12-signal-handler/main.c)

### Example 13: Send a signal

**Concept:** co-10. **Why:** kill signal makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-13-kill-signal`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-13-kill-signal/main.c)

### Example 14: Handle SIGTERM

**Concept:** co-09. **Why:** sigterm makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-14-sigterm`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-14-sigterm/main.c)

### Example 15: SIGKILL boundary

**Concept:** co-10. **Why:** sigkill makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-15-sigkill`.

**Observe:** Use `strace -e signal=all ./example` and identify delivery separately from handler work.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-15-sigkill/main.c)

### Example 16: Inspect with ps

**Concept:** co-29. **Why:** ps inspect makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-16-ps-inspect`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-16-ps-inspect/main.c)

### Example 17: Inspect with top

**Concept:** co-29. **Why:** top inspect makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-17-top-inspect`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-17-top-inspect/main.c)

### Example 18: Read proc status

**Concept:** co-28. **Why:** proc status makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-18-proc-status`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-18-proc-status/main.c)

### Example 19: List proc descriptors

**Concept:** co-28. **Why:** proc fd makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-19-proc-fd`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-19-proc-fd/main.c)

### Example 20: Read proc maps

**Concept:** co-28. **Why:** proc maps makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-20-proc-maps`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-20-proc-maps/main.c)

### Example 21: Open a descriptor

**Concept:** co-17. **Why:** fd open makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-21-fd-open`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-21-fd-open/main.c)

### Example 22: Inherit a descriptor

**Concept:** co-17. **Why:** fd inheritance makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-22-fd-inheritance`.

**Observe:** Trace it with `strace -f ./example` and match the syscall result to the source annotation.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-22-fd-inheritance/main.c)

### Example 23: Check permissions

**Concept:** co-20. **Why:** permissions check makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-23-permissions-check`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-23-permissions-check/main.c)

### Example 24: Change permissions

**Concept:** co-20. **Why:** chmod makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-24-chmod`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-24-chmod/main.c)

### Example 25: Inspect an inode

**Concept:** co-18. **Why:** stat inode makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-25-stat-inode`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-25-stat-inode/main.c)

### Example 26: List mounts

**Concept:** co-21. **Why:** mount list makes one Linux OS contract visible with a small, runnable probe.

**Run:** `cc -std=c11 -Wall -Wextra -Werror main.c -o example && ./example` from `learning/code/ex-26-mount-list`.

**Observe:** Inspect its live PID using `ps` and `/proc/$PID/status` rather than assuming fixed output.

**Change:** alter one input, rerun, and explain which kernel-visible state changed. [Source](./code/ex-26-mount-list/main.c)

---

← Previous: [Learning overview](./overview.md) · Next: [Intermediate](./intermediate.md) →

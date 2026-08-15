---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Retrieval practice

1. Explain why `fork()` returns twice and why only the parent calls `waitpid()`.
2. Predict which file descriptors survive `fork` and which survive `exec` with `FD_CLOEXEC`.
3. Given a `Z` process state, identify the missing operation and safely fix it.
4. Contrast a pipe's byte stream with shared `mmap` memory and a Unix-domain socket.
5. Read one `strace` line and name the user-space intent and kernel result.
6. Use `/proc/PID/maps` to find an anonymous mapped region without treating addresses as stable.
7. State why a signal handler may only do async-signal-safe work.
8. Say what `nice` biases and what it does not guarantee.

## Katas

1. Change ex-09 so the child exits 7; assert that the parent reports 7.
2. Add `O_CLOEXEC` to a descriptor experiment and prove it disappears after `exec`.
3. Replace polling in ex-30 with a blocked signal plus `sigsuspend`.
4. Make ex-35 deliberately race, then explain why a shared mapping alone is not synchronization.
5. Trace the capstone with `strace -f -e trace=process,signal,pipe,mmap` and annotate five calls.

## Self-check

- [ ] I can distinguish a syscall from a library wrapper.
- [ ] I can build and observe fork/exec/wait without leaking a child.
- [ ] I can choose pipe, socket, or shared memory deliberately.
- [ ] I can use `/proc`, `ps`, and `strace` as evidence, not guesses.

# 79 · Linux OS (By Example, C + shell †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · C + shell † · Learn 179 / Drill 279 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the Linux OS from the inside — kernel vs user space, syscalls, the process model
(fork/exec/wait), signals, virtual memory/paging, filesystems (inodes/fd/VFS), scheduling, and IPC —
observed from C + shell tooling (`/proc`, `strace`, `ps`/`top`). The app-developer view is
[`76-linux-app-development`](./76-linux-app-development.md); cross-OS contrast is
[`80-windows-os`](./80-windows-os.md).

## Why this exists · the big idea

- **The problem before the solution**: every program you run is lied to by the kernel — it believes it owns
  the CPU and all of memory — and when performance, concurrency, or a crash forces you underneath that
  illusion, you need to know what the OS is actually doing. This topic goes inside.
- **Keep-this-if-you-forget-everything**: the kernel provides mechanism — fork/exec, virtual memory, the
  VFS, scheduling — through a small syscall interface, and user space decides policy on top; the boundary
  between them is the whole design of the OS.
- **Big ideas touched**: `mechanism-vs-policy` — the kernel supplies the machinery (process creation,
  paging, fd/VFS) while leaving what and when to user space, and the syscall boundary is that split made
  concrete; `layering-and-leaks` — virtual memory and the process abstraction hide the hardware until
  paging, context switches, or `strace` make the layer visible.

## Prerequisites

- **Prior topics**: [topic 78 Just Enough C](./78-just-enough-c.md) (the language for syscalls) and
  [topic 5 Just Enough Bash](./05-just-enough-bash.md) (`/proc`, `ps`,
  `strace`).
- **Tools & environment**: a **Linux** machine (or VM/WSL2); **gcc/clang** + make; `strace`, `/proc`,
  `ps`/`top`; Neovim/VSCode (DD-17).
- **Assumed knowledge**: C pointers + structs + a `make` build (topic 78); shell process/job basics
  (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: kernel-vs-user space, syscalls (fork/exec/wait, signals, `mmap`), virtual
  memory/paging, filesystems (inodes, fd, VFS, permissions, mounts), `/proc`, `ps`/`top`, `strace` are
  evergreen OS interfaces/terminology, unchanged. The file pins no kernel/distro version — good; nothing to
  correct.

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every syscall/interface claim below traces to a `man7.org` / `kernel.org` primary source; two
staleness corrections are flagged for the authoring pass.

- **Process control** — `[Verified]` `fork(2)` creates a child (returns 0 in child, child PID in parent);
  `execve(2)` replaces the process image — **its first parameter is named `path`** (a corrected detail: it
  is NOT `pathname`); `wait(2)`/`waitpid(2)` reap children and yield exit status via `WEXITSTATUS`
  (man7.org/linux/man-pages/man2/fork.2, execve.2, wait.2). The `exec*` family wrappers are in
  man7.org/…/man3/exec.3.
- **Signals** — `[Verified]` `signal(7)` documents standard + real-time signals; `sigaction(2)` is the
  reliable handler-installation API; SIGKILL/SIGSTOP cannot be caught or ignored; `kill(2)` sends signals
  (man7.org/linux/man-pages/man7/signal.7, man2/sigaction.2, man2/kill.2).
- **Memory** — `[Verified]` `mmap(2)` maps files or anonymous memory (`MAP_SHARED`/`MAP_ANONYMOUS`);
  `brk(2)`/`sbrk(3)` adjust the heap break; virtual memory/demand paging are the model
  (man7.org/linux/man-pages/man2/mmap.2, man2/brk.2).
- **Filesystem & fds** — `[Verified]` `open(2)` returns a file descriptor (a per-process fd-table index);
  `stat(2)` exposes inode + mode bits; the VFS presents a uniform `read`/`write` interface across
  filesystems; `chmod(2)` changes permissions (man7.org/linux/man-pages/man2/open.2, stat.2, chmod.2).
- **IPC** — `[Verified]` `pipe(2)` creates a unidirectional byte stream; `shm_open(3)`/`mmap` back POSIX
  shared memory; `socket(2)`/`socketpair(2)` provide Unix-domain IPC (man7.org/linux/man-pages/man2/pipe.2,
  man3/shm_open.3, man2/socketpair.2).
- **Scheduling** — `[Verified]` **the current Linux CPU scheduler is EEVDF** (Earliest Eligible Virtual
  Deadline First), which **replaced CFS (the Completely Fair Scheduler) as the default in Linux 6.6**
  (2023) — authored content must NOT present CFS as the current scheduler; treat scheduling at the
  concept level (time-slicing, context switches, `nice` priority) and name EEVDF as current
  (kernel.org sched docs, man7.org/…/man7/sched.7). `[Needs Verification]` at authoring — re-confirm the
  scheduler name against the running kernel's docs.
- **Observation tools** — `[Verified]` `/proc` exposes per-process state (`/proc/<pid>/status`, `/fd`,
  `/maps`, `/cmdline`); `ps`/`top` list processes; `strace(1)` traces syscalls
  (man7.org/linux/man-pages/man5/proc.5, man1/strace.1).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · kernel-vs-user** — code runs in privileged kernel space or unprivileged user space; the boundary protects the machine.
- **co-02 · syscalls** — a system call traps from user space into the kernel to request a service.
- **co-03 · syscall-observe** — `strace` observes the syscalls a program makes.
- **co-04 · process-model** — a process has a PID and sits in a parent/child process tree.
- **co-05 · fork** — `fork()` creates a child process (returns 0 in the child, the child PID in the parent).
- **co-06 · exec** — `execve()`/`exec*` replaces the current process image with a new program.
- **co-07 · wait** — `wait()`/`waitpid()` reaps a child and retrieves its exit status.
- **co-08 · fork-exec-wait** — the fork→exec→wait pattern is how a shell launches a command.
- **co-09 · signals** — signals (SIGINT/SIGTERM/SIGKILL) asynchronously notify a process; handlers respond.
- **co-10 · signal-delivery** — `kill()` sends a signal; each signal has a default disposition.
- **co-11 · process-states** — a process is running/sleeping/stopped/zombie; an unreaped child is a zombie.
- **co-12 · virtual-memory** — each process sees a private virtual address space, not physical memory.
- **co-13 · paging** — memory is paged; demand paging brings pages in on first access.
- **co-14 · address-space-layout** — the address space holds text/data/heap/stack segments.
- **co-15 · mmap** — `mmap` maps files or anonymous memory into the address space.
- **co-16 · brk-heap** — `brk`/`sbrk` grow the heap; `malloc` builds on them (and `mmap`).
- **co-17 · file-descriptors** — a file descriptor indexes the process's open-file table.
- **co-18 · inodes** — an inode holds a file's metadata on disk, separate from its name.
- **co-19 · vfs** — the VFS gives a uniform `read`/`write` interface across different filesystems.
- **co-20 · permissions** — file mode bits + ownership control access.
- **co-21 · mounts** — filesystems are attached to the tree at mount points.
- **co-22 · pipes** — `pipe()` creates a unidirectional byte stream between processes.
- **co-23 · shared-memory** — shared-memory IPC lets processes share a memory region.
- **co-24 · sockets-ipc** — Unix-domain sockets carry bidirectional IPC.
- **co-25 · scheduling** — the scheduler (EEVDF, which replaced CFS in Linux 6.6) time-slices the CPU via context switches.
- **co-26 · threads-vs-processes** — threads share one address space; processes each have their own.
- **co-27 · priorities** — `nice` values bias a process's scheduling priority.
- **co-28 · proc-filesystem** — `/proc` exposes live kernel and per-process state as files.
- **co-29 · process-tools** — `ps`/`top` observe running processes from the shell.
- **co-30 · os-theory** — these Linux mechanisms are one implementation of universal OS concepts (process, VM, scheduling, FS, IPC) that recur in every OS.

## Tensions & trade-offs — when NOT to reach for this

- **Observing from user space vs writing a kernel module**: this topic teaches the OS from user space —
  syscalls, `/proc`, `strace` — which is where a working engineer needs fluency; writing kernel code is a
  substantially higher-cost, higher-risk path that is out of scope here and rarely the right first move.
- **Threads vs processes**: threads share an address space and are cheaper to create and context-switch,
  but that sharing is exactly what makes concurrent bugs (races, corrupted shared state) possible — a
  process boundary trades that risk for isolation at the cost of IPC and a heavier `fork`.
- **When NOT to use it**: hand-rolling process/signal/IPC code when a higher-level abstraction (a language
  runtime, a message queue, a supervised process manager) already solves the problem safely. Reach for
  raw `fork`/`signal`/shared memory only when you are building the infrastructure itself, not an
  application on top of it.

## Lineage — why it beat the alternative

- Early Unix systems ran cooperative, single-tasking programs with no memory protection between them — a
  crash or a runaway process could take down the whole machine. The process model — an isolated virtual
  address space per program, mediated entirely through a small syscall interface — won because it lets
  many untrusted programs share one machine safely, at the cost of a real context-switch and IPC tax.
  Linux's specific choices — the VFS's uniform file interface, `fork`+`exec` as two separate steps instead
  of one combined "spawn" call, and (currently) EEVDF over CFS for scheduling — are refinements of that
  same tradeoff, still visible today in [`76-linux-app-development`](./76-linux-app-development.md)'s use
  of the very same syscalls this topic teaches directly.

## Worked examples

Colocated under `linux-os/learning/code/`; C + shell against a live Linux system (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · hello-syscall** — a C `write()` syscall directly — verify output crosses the user/kernel boundary. (co-02, co-01)
- **ex-02 · strace-hello** — `strace` a hello program — verify the syscalls shown. (co-03, co-02)
- **ex-03 · getpid** — `getpid()` prints the PID — verify it matches `ps`. (co-04)
- **ex-04 · fork-basic** — `fork()` creates a child — verify two processes print. (co-05)
- **ex-05 · fork-return** — fork's return value (0 in child, PID in parent) — verify the branch. (co-05)
- **ex-06 · exec-basic** — `execve` replaces the image — verify the new program runs. (co-06)
- **ex-07 · exec-ls** — `fork` then `exec` `ls` — verify `ls` output. (co-06, co-05)
- **ex-08 · wait-child** — `wait()` reaps a child — verify the parent gets the exit status. (co-07)
- **ex-09 · fork-exec-wait** — the full fork→exec→wait pattern — verify orchestration. (co-08)
- **ex-10 · exit-status** — read a child's exit status (`WEXITSTATUS`) — verify the code. (co-07)
- **ex-11 · zombie** — an unreaped child becomes a zombie — verify `ps` shows `Z`. (co-11, co-07)
- **ex-12 · signal-handler** — install a SIGINT handler — verify Ctrl-C is caught. (co-09)
- **ex-13 · kill-signal** — send a signal with `kill()` — verify the target reacts. (co-10)
- **ex-14 · sigterm** — handle SIGTERM — verify clean shutdown. (co-09)
- **ex-15 · sigkill** — SIGKILL can't be caught — verify the process dies. (co-09, co-10)
- **ex-16 · ps-inspect** — `ps` lists processes — verify the target appears. (co-29)
- **ex-17 · top-inspect** — `top` watches resource use — verify live stats. (co-29)
- **ex-18 · proc-status** — read `/proc/<pid>/status` — verify process fields. (co-28)
- **ex-19 · proc-fd** — list `/proc/<pid>/fd` — verify open descriptors. (co-28, co-17)
- **ex-20 · proc-maps** — read `/proc/<pid>/maps` — verify the memory map. (co-28, co-14)
- **ex-21 · fd-open** — `open()` returns a file descriptor — verify the fd number. (co-17)
- **ex-22 · fd-inheritance** — a child inherits the parent's fds — verify shared access. (co-17, co-05)
- **ex-23 · permissions-check** — `stat` a file's mode bits — verify the permissions. (co-20)
- **ex-24 · chmod** — `chmod` changes permissions — verify the new mode. (co-20)
- **ex-25 · stat-inode** — `stat` shows the inode number — verify it. (co-18)
- **ex-26 · mount-list** — `mount`/`/proc/mounts` lists mounts — verify a filesystem. (co-21)

### Intermediate

- **ex-27 · pipe-basic** — `pipe()` between parent and child — verify a byte crosses. (co-22)
- **ex-28 · pipe-dup2** — `dup2` a pipe onto stdout — verify redirection. (co-22, co-17)
- **ex-29 · pipe-shell-emulate** — emulate `a | b` with pipe+fork+exec — verify the pipeline. (co-22, co-08)
- **ex-30 · signal-between-processes** — a parent signals a child to proceed — verify coordination. (co-09, co-10)
- **ex-31 · sigaction** — `sigaction` for reliable signal handling — verify the handler. (co-09)
- **ex-32 · signal-mask** — block/unblock a signal — verify deferral. (co-09)
- **ex-33 · mmap-anon** — `mmap` anonymous memory — verify read/write. (co-15)
- **ex-34 · mmap-file** — `mmap` a file — verify the mapping reflects the file. (co-15)
- **ex-35 · mmap-shared** — `MAP_SHARED` between processes — verify shared writes. (co-15, co-23)
- **ex-36 · shm-open** — `shm_open` a shared segment — verify it's created. (co-23)
- **ex-37 · shm-ipc** — two processes share data via shm — verify the value crosses. (co-23)
- **ex-38 · unix-socket** — a Unix-domain socket — verify a message. (co-24)
- **ex-39 · socketpair** — `socketpair()` for a bidirectional channel — verify both directions. (co-24)
- **ex-40 · vfs-same-api** — read a regular file and a `/proc` file with the same `read()` — verify the VFS uniformity. (co-19, co-17)
- **ex-41 · heap-brk** — `sbrk` grows the heap — verify the new break. (co-16)
- **ex-42 · malloc-strace** — `strace` `malloc` to see brk/mmap — verify the syscalls. (co-16, co-03)
- **ex-43 · address-space-segments** — print addresses of code/data/heap/stack — verify the virtual-memory layout order. (co-14, co-12)
- **ex-44 · page-fault** — trigger a page fault on a fresh `mmap` — verify demand paging. (co-13, co-15)
- **ex-45 · strace-openfile** — `strace` a file-opening program — verify open/read/close. (co-03)
- **ex-46 · strace-count** — `strace -c` syscall summary — verify the counts. (co-03)
- **ex-47 · ps-tree** — `pstree`/`ps --forest` — verify the process tree. (co-04, co-29)
- **ex-48 · nice-priority** — run with `nice` — verify the priority. (co-27)
- **ex-49 · thread-vs-process** — `pthread_create` vs `fork` memory sharing — verify threads share, processes don't. (co-26)
- **ex-50 · context-switch-count** — `/proc/<pid>/status` `voluntary_ctxt_switches` — verify it. (co-25, co-28)
- **ex-51 · zombie-reap** — reap a zombie with `wait` — verify it disappears. (co-11, co-07)
- **ex-52 · orphan-reparent** — an orphan is reparented to init — verify PPID becomes 1. (co-04, co-05)
- **ex-53 · proc-cmdline** — `/proc/<pid>/cmdline` — verify the args. (co-28)
- **ex-54 · signalfd** — `signalfd` to read signals as fds — verify the integration. (co-09, co-17)

### Advanced

- **ex-55 · shell-mini** — a mini-shell: read, fork, exec, wait — verify command execution. (co-08, co-22)
- **ex-56 · shell-pipe** — the mini-shell handles `a | b` — verify the pipeline. (co-22, co-08)
- **ex-57 · shell-signal** — the mini-shell handles Ctrl-C without dying — verify the handler. (co-09, co-08)
- **ex-58 · producer-consumer-shm** — producer/consumer over shared memory + a semaphore — verify sync. (co-23, co-24)
- **ex-59 · mmap-large-file** — `mmap` a large file + random access — verify paging. (co-15, co-13)
- **ex-60 · copy-on-write** — fork's COW: child writes trigger a copy — verify separate pages. (co-05, co-13)
- **ex-61 · fd-leak-detect** — detect an fd leak via `/proc/<pid>/fd` — verify the growing count. (co-17, co-28)
- **ex-62 · strace-network** — `strace` a socket program — verify connect/send syscalls. (co-03, co-24)
- **ex-63 · signal-race** — a signal-safe handler using only async-signal-safe calls — verify correctness. (co-09)
- **ex-64 · waitpid-nonblock** — `waitpid` with `WNOHANG` — verify non-blocking reaping. (co-07)
- **ex-65 · process-group** — `setpgid` + signal a process group — verify group delivery. (co-04, co-10)
- **ex-66 · daemon-double-fork** — a daemon via double-fork + `setsid` — verify detachment. (co-05, co-08)
- **ex-67 · mount-namespace** — an `unshare` mount namespace (intuition) — verify isolation. (co-21)
- **ex-68 · vfs-proc-vs-disk** — compare a `/proc` read vs a disk read via `strace` — verify the same syscalls. (co-19, co-03)
- **ex-69 · scheduler-observe** — observe scheduling with time-slicing under load — verify fairness (EEVDF). (co-25)
- **ex-70 · top-threads** — `top -H` shows threads — verify the per-thread view. (co-26, co-29)
- **ex-71 · mmap-shared-counter** — a shared counter in `mmap` incremented by two processes — verify the total. (co-15, co-23)
- **ex-72 · pipe-deadlock** — a full-pipe deadlock + its fix — verify the corrected flow. (co-22)
- **ex-73 · inode-hardlink** — a hard link shares an inode — verify the same inode number. (co-18)
- **ex-74 · permission-denied** — a permission-denied `open` → `EACCES` — verify errno. (co-20, co-02)
- **ex-75 · strace-signal** — `strace` shows signal delivery — verify the trace. (co-03, co-09)
- **ex-76 · full-ipc-slice** — fork children coordinated by signals + a pipe + shared memory — verify the whole. (co-08, co-09, co-22, co-23)
- **ex-77 · integration-observe-slice** — the IPC program observed via `/proc` + `ps` + `strace` + its `mmap` — verify tooling reflects state. (co-28, co-29, co-03, co-15)
- **ex-78 · capstone-process-tour** — a C program: fork/exec/wait children, coordinate with signals + a pipe, share via shared memory, then observe via `/proc`, `ps`, `strace`, and `mmap` — verify process control, IPC, and tooling all reflect the expected syscalls/state. (co-08, co-09, co-22, co-23, co-28, co-29, co-03, co-15, co-30)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: write a small C program that spawns children (`fork`/`exec`/`wait`), coordinates them with
  signals + a pipe and shares data via shared memory, then observe the whole thing from the shell —
  inspecting `/proc`, tracing its syscalls with `strace`, and confirming its memory map — a hands-on tour
  of the process/memory/IPC model.
- **Concepts exercised**: [ ] `fork`/`exec`/`wait` process control (co-08) [ ] signal handling (co-09)
  [ ] a pipe between processes (co-22) [ ] shared-memory IPC (co-23) [ ] `/proc` + `ps` inspection
  (co-28, co-29) [ ] `strace` syscall reading + an `mmap` view (co-03, co-15).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a parent that `fork`/`exec`/`wait`s a child + handles a signal. Verify
     the child runs, the parent reaps it, and the signal is handled.
  2. Add a pipe + a shared-memory segment between two processes. Verify data crosses the pipe and the shared
     segment.
  3. Observe: inspect the running process via `/proc` + `ps`, `strace` it, and view its `mmap`. Verify the
     `strace` output shows the expected syscalls and `/proc` reflects the process state.
- **Acceptance criteria**: process control + signals + pipe + shared memory all work; `/proc`/`ps`
  inspection and `strace` show the expected syscalls; the memory map is explained.
- **Done bar**: runnable end-to-end (Linux) + observed via tooling + web-verified.

## Read more

**Books**

- **The Linux Programming Interface** — Michael Kerrisk (2010, No Starch Press). The canonical, comprehensive Linux/UNIX systems-programming reference.
- **How Linux Works**, 3rd ed. — Brian Ward (2021, No Starch Press). The widely recommended canonical guide to Linux internals and administration for working engineers.
- **Linux Kernel Development**, 3rd ed. — Robert Love (2010, Addison-Wesley). A classic, accessible guide to kernel internals by a Linux/Android kernel engineer.
- **Advanced Programming in the UNIX Environment**, 3rd ed. — W. Richard Stevens & Stephen A. Rago (2013, Addison-Wesley). "APUE" — the classic, still-foundational UNIX/Linux systems-programming reference.

**Papers & articles**

- **The Linux man-pages project** — Michael Kerrisk et al., official (kernel.org project). The canonical, free reference for Linux syscalls and library calls. <https://man7.org/linux/man-pages/>

---

← Previous: [78 · Just Enough C](./78-just-enough-c.md) · Next: [80 · Windows OS](./80-windows-os.md) →

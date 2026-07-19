# 80 · Windows OS (By Example, C + PowerShell †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · C + PowerShell † · Learn 180 /
Drill 280 · Nvim-ready Partial · VSCode-ready Partial. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the Windows OS from the inside — user vs kernel mode, the Win32 API, the object/handle
model, the registry, processes/threads (`CreateProcess`), memory management, Win32 synchronization,
NTFS/async I/O — observed from C (Win32) + PowerShell tooling. The deliberate cross-OS contrast to
[`79-linux-os`](./79-linux-os.md).

## Why this exists · the big idea

- **The problem before the solution**: the same OS jobs — spawn a process, share memory, synchronize
  threads — that Linux does with fds and `fork`, Windows does with handles, objects, and `CreateProcess`;
  an engineer who knows only one model is blind on the other machine. This topic supplies the second lens.
- **Keep-this-if-you-forget-everything**: Windows is an object-and-handle OS — nearly every kernel resource
  is an object you hold by handle — which is the deep structural contrast to Linux's
  file-descriptor-and-`fork` model.
- **Big ideas touched**: `mechanism-vs-policy` — the Win32 API and object manager are the mechanism the OS
  exposes, and how you compose `CreateProcess`, handles, and sync primitives is your policy;
  `layering-and-leaks` — user-mode code sits on the Win32 subsystem over the kernel, and the handle/object
  model plus overlapped I/O are where that layering surfaces in your code.

## Prerequisites

- **Prior topics**: [topic 78 Just Enough C](./78-just-enough-c.md) (the language for Win32 calls),
  [topic 79 Linux OS](./79-linux-os.md) (the OS-concept baseline to contrast), and
  [topic 5 Just Enough Bash](./05-just-enough-bash.md) (shell/PowerShell
  fluency).
- **Tools & environment**: a **Windows** machine; a C toolchain (MSVC or MinGW) for Win32; **PowerShell**;
  Task Manager / Process Explorer for inspection; Neovim/VSCode (DD-17).
- **Assumed knowledge**: C pointers + structs (topic 78); the process/memory/IPC model from Linux to
  contrast (topic 79); shell basics (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: user-vs-kernel mode, Win32 API (`CreateProcess`, handles, object model, registry,
  subsystems), Win32 sync primitives (mutex/event/critical section), NTFS concepts, overlapped I/O,
  PowerShell inspection, and Task Manager / Process Explorer (Sysinternals) are evergreen/unchanged. The
  file pins no Windows release number — good; nothing to correct.

### DD-35 primary-source citations (fetched-and-read)

Per DD-35, every Win32 API / concept claim below traces to a `learn.microsoft.com` primary page; these
are decades-stable interfaces (minimum-supported-client Windows XP/2000 on the reference pages).

- **User/kernel mode** — `[Verified]` "Applications operate in user mode. Core operating system components
  function in kernel mode"; each user process gets a private virtual address space + private handle table
  (learn.microsoft.com/windows-hardware/drivers/gettingstarted/user-mode-and-kernel-mode).
- **Win32 API** — `[Verified]` the "Windows API" (formerly "Win32 API") targets all Windows versions; the
  URL namespace is `learn.microsoft.com/windows/win32` (…/apiindex/windows-api-list).
- **Object/handle model** — `[Verified]` Windows is _object-based_: files, processes, threads, mutexes,
  registry keys, etc. are kernel objects held by a unified `HANDLE`; `CloseHandle` "invalidates the handle,
  decrements the object's handle count, and performs object retention checks" — closing a handle does NOT
  terminate the underlying process/thread (…/api/handleapi/nf-handleapi-closehandle,
  …/windows-hardware/drivers/kernel/windows-kernel-mode-object-manager). This is the structural contrast
  to Linux fds (which are a VFS abstraction) — [`79-linux-os`](./79-linux-os.md).
- **CreateProcess** — `[Verified]` "Creates a new process and its primary thread. The new process runs in
  the security context of the calling process"; each process starts with one primary thread
  (…/api/processthreadsapi/nf-processthreadsapi-createprocessa, …/procthread/about-processes-and-threads).
  Windows has NO `fork()` equivalent — `CreateProcess` always starts a clean image (closest to POSIX
  `posix_spawn`); the "no fork" contrast is `[Needs Verification]`-grade at the verbatim level (best primary
  source: the MS Research "A fork() in the road" paper, not fetched verbatim) — present it as a well-
  established design contrast, not a quoted claim.
- **Threads** — `[Verified]` `CreateThread` "Creates a thread to execute within the virtual address space
  of the calling process"; Windows uses preemptive multitasking
  (…/api/processthreadsapi/nf-processthreadsapi-createthread).
- **Memory** — `[Verified]` `VirtualAlloc` "Reserves, commits, or changes the state of a region of pages…
  Memory allocated by this function is automatically initialized to zero" (`MEM_RESERVE`/`MEM_COMMIT`);
  `HeapCreate`/`HeapAlloc` build on `VirtualAlloc` for large blocks; the _working set_ = pages recently
  referenced (…/api/memoryapi/nf-memoryapi-virtualalloc, …/api/heapapi/nf-heapapi-heapcreate;
  working-set term confirmed via `Get-Process` WS(M) docs).
- **Synchronization** — `[Verified]` `CreateMutex` "Creates or opens a named or unnamed mutex object" (usable
  cross-process); `CreateEvent` (manual/auto-reset); `InitializeCriticalSection` — VERBATIM: "The threads of
  a single process can use a critical section object for mutual-exclusion synchronization… For similar
  synchronization between the threads of different processes, use a mutex object." Note: a critical section
  is NOT a kernel object (userspace fast path) (…/api/synchapi/nf-synchapi-createmutexa, …-createeventa,
  …-initializecriticalsection).
- **File / async I/O** — `[Verified]` `CreateFile` "Creates or opens a file or I/O device… returns a handle"
  (returns `INVALID_HANDLE_VALUE`, not `NULL`, on failure); overlapped (async) I/O uses `FILE_FLAG_OVERLAPPED`
  - an `OVERLAPPED` struct; NTFS supports alternate data streams + compression/encryption
    (…/api/fileapi/nf-fileapi-createfilea, …/fileio/synchronous-and-asynchronous-i-o).
- **Registry** — `[Verified]` a hierarchical key/subkey/value tree; `RegOpenKeyEx` "Opens the specified
  registry key" + `RegQueryValueEx` "Retrieves the type and data for the specified value name"; note these
  live in `Advapi32.dll` (not `Kernel32`) (…/api/winreg/nf-winreg-regopenkeyexa, …-regqueryvalueexa,
  …/sysinfo/structure-of-the-registry).
- **Tooling** — `[Verified]` PowerShell `Get-Process` (WS(M)/memory columns) and `Get-Service` (Windows-only);
  Sysinternals Process Explorer shows a process's open handles/loaded DLLs
  (learn.microsoft.com/powershell/module/microsoft.powershell.management/get-process, …-get-service,
  learn.microsoft.com/sysinternals/downloads/process-explorer).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · user-kernel-mode** — applications run in user mode; core OS components run in privileged kernel mode.
- **co-02 · win32-api** — the Win32 (Windows) API is the C interface user-mode code calls into.
- **co-03 · subsystems** — user code sits on the Win32 subsystem layered over the kernel.
- **co-04 · object-handle-model** — nearly every kernel resource is an object held via a unified `HANDLE`.
- **co-05 · handle-lifecycle** — `CloseHandle` decrements an object's handle count; the object is freed when the last handle closes (closing a handle ≠ ending the process/thread).
- **co-06 · createprocess** — `CreateProcess` creates a new process and its primary thread.
- **co-07 · process-primary-thread** — every process starts with exactly one primary thread.
- **co-08 · createthread** — `CreateThread` creates a thread inside the process's address space.
- **co-09 · thread-scheduling** — Windows preemptively schedules threads (with priorities).
- **co-10 · virtualalloc** — `VirtualAlloc` reserves/commits zero-initialized virtual memory.
- **co-11 · reserve-commit** — `MEM_RESERVE` reserves address space; `MEM_COMMIT` backs it with storage.
- **co-12 · heaps** — `HeapCreate`/`HeapAlloc` manage heap allocations atop `VirtualAlloc`.
- **co-13 · working-set** — the working set is the pages of a process recently in memory.
- **co-14 · mutex** — `CreateMutex` provides mutual exclusion, usable across processes when named.
- **co-15 · event** — `CreateEvent` signals between threads (manual- or auto-reset).
- **co-16 · critical-section** — `InitializeCriticalSection` is an in-process, lightweight lock (not a kernel object).
- **co-17 · wait-functions** — `WaitForSingleObject`/`WaitForMultipleObjects` block on a synchronization object.
- **co-18 · createfile** — `CreateFile` opens a file/device and returns a `HANDLE` (`INVALID_HANDLE_VALUE` on failure).
- **co-19 · sync-async-io** — I/O is synchronous or overlapped (async) via `FILE_FLAG_OVERLAPPED` + an `OVERLAPPED` struct.
- **co-20 · ntfs** — NTFS supports alternate data streams and per-file compression/encryption.
- **co-21 · registry** — the registry is a hierarchical hive → key → subkey → value tree.
- **co-22 · registry-api** — `RegOpenKeyEx`/`RegQueryValueEx` read the registry (in `Advapi32`).
- **co-23 · powershell-getprocess** — PowerShell `Get-Process` inspects running processes.
- **co-24 · powershell-getservice** — `Get-Service` inspects Windows services (Windows-only).
- **co-25 · process-explorer** — Sysinternals Process Explorer shows a process's open handles and loaded DLLs.
- **co-26 · task-manager** — Task Manager gives a process/resource overview.
- **co-27 · handle-vs-fd** — a Windows `HANDLE` (any object) contrasts with a Linux file descriptor (a VFS abstraction).
- **co-28 · createprocess-vs-fork** — `CreateProcess` starts a clean image (no `fork`), contrasting Linux fork/exec.
- **co-29 · object-manager-vs-vfs** — the Windows Object Manager (all object types) contrasts with the Linux VFS (files).
- **co-30 · os-theory** — Win32's handles/objects/working-sets are one implementation of universal OS concepts also seen in [`79-linux-os`](./79-linux-os.md).

## Worked examples

Colocated under `windows-os/learning/code/`; C (Win32) + PowerShell on Windows (DD-20/DD-30). Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · win32-hello** — a C Win32 program (console/`MessageBox`) — verify it runs in user mode via the Win32 subsystem. (co-02, co-01, co-03)
- **ex-02 · getcurrentprocessid** — `GetCurrentProcessId` — verify it matches Task Manager. (co-02)
- **ex-03 · createprocess-basic** — `CreateProcess` launches `cmd`/notepad — verify the child starts. (co-06)
- **ex-04 · createprocess-wait** — wait on the child's process handle — verify the parent waits. (co-06, co-17)
- **ex-05 · primary-thread** — the child starts with one primary thread — verify via inspection. (co-07)
- **ex-06 · handle-return** — `CreateProcess` returns handles in `PROCESS_INFORMATION` — verify the handles. (co-04, co-06)
- **ex-07 · closehandle** — `CloseHandle` after use — verify no leak. (co-05)
- **ex-08 · handle-count** — observe the object's handle count — verify it drops on close. (co-05)
- **ex-09 · createthread-basic** — `CreateThread` runs a function — verify the thread runs. (co-08)
- **ex-10 · thread-wait** — `WaitForSingleObject` on the thread handle — verify it joins. (co-08, co-17)
- **ex-11 · multiple-threads** — several threads — verify concurrent execution. (co-08, co-09)
- **ex-12 · getprocess-ps** — `Get-Process` in PowerShell — verify the target appears. (co-23)
- **ex-13 · getprocess-filter** — `Get-Process` by name — verify filtering. (co-23)
- **ex-14 · getservice-ps** — `Get-Service` — verify a service is listed (Windows-only). (co-24)
- **ex-15 · task-manager** — Task Manager shows the process — verify CPU/memory. (co-26)
- **ex-16 · process-explorer-handles** — Process Explorer handle view — verify open handles. (co-25)
- **ex-17 · createfile-open** — `CreateFile` opens a file, returns a `HANDLE` — verify the handle. (co-18)
- **ex-18 · createfile-fail** — `CreateFile` on a missing file → `INVALID_HANDLE_VALUE` — verify the error. (co-18)
- **ex-19 · readfile** — `ReadFile` via a handle — verify contents. (co-18)
- **ex-20 · writefile** — `WriteFile` via a handle — verify persistence. (co-18)
- **ex-21 · virtualalloc-basic** — `VirtualAlloc` commit memory — verify it's zeroed. (co-10)
- **ex-22 · virtualalloc-write** — write to the allocated region — verify read-back. (co-10)
- **ex-23 · reg-open** — `RegOpenKeyEx` a key — verify it opens. (co-22)
- **ex-24 · reg-query** — `RegQueryValueEx` a value — verify the data. (co-22)
- **ex-25 · registry-tree** — the HKLM/HKCU hive structure — verify a subkey. (co-21)
- **ex-26 · reg-ps** — PowerShell `Get-ItemProperty` on the registry — verify a value. (co-21, co-23)

### Intermediate

- **ex-27 · mutex-create** — `CreateMutex` — verify it's created. (co-14)
- **ex-28 · mutex-lock** — `WaitForSingleObject` + `ReleaseMutex` — verify mutual exclusion. (co-14, co-17)
- **ex-29 · mutex-two-threads** — two threads guarded by a mutex — verify no data race. (co-14, co-08)
- **ex-30 · named-mutex-crossprocess** — a named mutex across two processes — verify cross-process sync. (co-14, co-06)
- **ex-31 · critical-section** — `InitializeCriticalSection` + Enter/Leave — verify mutual exclusion. (co-16)
- **ex-32 · critical-section-vs-mutex** — a critical section (in-process) vs a mutex (cross-process) — verify the distinction. (co-16, co-14)
- **ex-33 · event-create** — `CreateEvent` — verify it's created. (co-15)
- **ex-34 · event-signal** — `SetEvent` wakes a waiter — verify signaling. (co-15, co-17)
- **ex-35 · event-manual-reset** — a manual-reset event — verify it stays signaled. (co-15)
- **ex-36 · wait-multiple** — `WaitForMultipleObjects` — verify waiting on several. (co-17)
- **ex-37 · reserve-commit** — `VirtualAlloc` `MEM_RESERVE` then `MEM_COMMIT` — verify two-step allocation. (co-11, co-10)
- **ex-38 · heap-create** — `HeapCreate` + `HeapAlloc` — verify allocation. (co-12)
- **ex-39 · heap-on-virtualalloc** — a large `HeapAlloc` uses `VirtualAlloc` — verify the layering. (co-12, co-10)
- **ex-40 · working-set** — `Get-Process` WS(M) working set — verify it reflects usage. (co-13, co-23)
- **ex-41 · overlapped-io** — `CreateFile` `FILE_FLAG_OVERLAPPED` + `ReadFile` with `OVERLAPPED` — verify async I/O. (co-19, co-18)
- **ex-42 · sync-vs-async-io** — a synchronous vs overlapped read — verify the difference. (co-19)
- **ex-43 · ntfs-stream** — an NTFS alternate data stream via `CreateFile` — verify it's written. (co-20, co-18)
- **ex-44 · ntfs-attributes** — an NTFS compression/encryption attribute — verify it's set. (co-20)
- **ex-45 · createprocess-cmdline** — `CreateProcess` with a command line + args — verify the child gets them. (co-06)
- **ex-46 · process-tree-ps** — a process tree via PowerShell — verify parent/child. (co-23)
- **ex-47 · handle-inspect-ps** — inspect handles via Process Explorer — verify the open file handle. (co-25, co-18)
- **ex-48 · thread-priority** — `SetThreadPriority` — verify the scheduling bias. (co-09)
- **ex-49 · memory-inspect-ps** — `Get-Process` memory columns — verify the memory view. (co-13, co-23)
- **ex-50 · reg-write** — `RegSetValueEx` writes a value — verify it persists. (co-22)
- **ex-51 · service-query** — `Get-Service` status — verify running/stopped. (co-24)
- **ex-52 · duplicate-handle** — `DuplicateHandle` across processes — verify shared access. (co-04, co-05)
- **ex-53 · wait-timeout** — `WaitForSingleObject` with a timeout — verify the timeout path. (co-17)
- **ex-54 · close-all-handles** — close every handle a program opened — verify no leak in Process Explorer. (co-05, co-25)

### Advanced

- **ex-55 · process-plus-threads** — `CreateProcess` a child + two synchronized threads — verify orchestration. (co-06, co-08, co-14)
- **ex-56 · producer-consumer-event** — producer/consumer coordinated by events — verify sync. (co-15, co-08)
- **ex-57 · shared-memory-mapping** — `CreateFileMapping` + `MapViewOfFile` shared memory — verify IPC. (co-10, co-04)
- **ex-58 · overlapped-completion** — overlapped I/O with a completion event — verify async completion. (co-19, co-15)
- **ex-59 · handle-leak-demo** — a handle leak observed in Process Explorer + its fix — verify the count stabilizes. (co-05, co-25)
- **ex-60 · race-then-fix** — a data race then a critical-section fix — verify correctness. (co-16, co-08)
- **ex-61 · named-sync-two-procs** — a named event/mutex synchronizing two processes — verify cross-process. (co-14, co-15)
- **ex-62 · virtualalloc-guard** — a guard page via `VirtualAlloc` protection — verify the fault. (co-10, co-11)
- **ex-63 · registry-round-trip** — write then read a registry value — verify the round-trip. (co-22, co-21)
- **ex-64 · file-round-trip-handle** — handle-based write then read — verify the round-trip. (co-18)
- **ex-65 · ntfs-stream-round-trip** — write + read an ADS — verify the hidden stream. (co-20, co-18)
- **ex-66 · process-explorer-dll** — Process Explorer DLL view — verify loaded modules. (co-25)
- **ex-67 · powershell-cim** — a PowerShell CIM/WMI process query — verify richer detail. (co-23)
- **ex-68 · handle-vs-fd-contrast** — a `HANDLE` (thread/mutex/file) vs a Linux fd — verify the model contrast. (co-27)
- **ex-69 · createprocess-vs-fork-contrast** — `CreateProcess` (clean image) vs fork/exec — verify the contrast. (co-28)
- **ex-70 · objectmanager-vs-vfs-contrast** — the Object Manager (any object) vs the VFS (files) — verify the contrast. (co-29)
- **ex-71 · wait-object-uniformity** — `WaitForSingleObject` works on process/thread/mutex/event handles — verify the uniform handle model. (co-17, co-04)
- **ex-72 · thread-pool-intuition** — a small thread-pool pattern — verify work distribution. (co-08, co-09)
- **ex-73 · async-io-scale** — overlapped I/O on multiple files — verify concurrent I/O. (co-19)
- **ex-74 · memory-protection** — `VirtualProtect` changes page protection — verify the new access. (co-10)
- **ex-75 · inspect-matches-code** — PowerShell/Process Explorer inspection matches the running program — verify consistency. (co-23, co-25)
- **ex-76 · full-win32-slice** — `CreateProcess` + synchronized threads + handle-based overlapped I/O — verify the whole. (co-06, co-14, co-19, co-08)
- **ex-77 · integration-contrast-slice** — the Win32 program with a written Windows-vs-Linux contrast — verify the contrast is concrete. (co-27, co-28, co-29)
- **ex-78 · capstone-windows-tour** — a Win32 C program: `CreateProcess` a child, coordinate two threads with a mutex/critical section, do handle-based overlapped file I/O, inspect via PowerShell + Process Explorer, and write `contrast.md` — verify process/sync/IO work with no leak/race, inspection matches, and the contrast is concrete. (co-06, co-14, co-16, co-19, co-05, co-23, co-25, co-27, co-30)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: write a small Win32 C program that creates a child process (`CreateProcess`), coordinates two
  threads with a mutex/critical section, and does handle-based (overlapped) file I/O, then inspect it from
  PowerShell + Process Explorer — and write a short Windows-vs-Linux contrast against the topic-53 model.
- **Concepts exercised**: [ ] `CreateProcess` + the handle/object model (co-06, co-04) [ ] Win32 thread
  synchronization (mutex/critical section) (co-14, co-16) [ ] handle-based / overlapped file I/O (co-18, co-19)
  [ ] PowerShell + tooling inspection (co-23, co-25) [ ] a Windows-vs-Linux OS contrast (co-27, co-28, co-29).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a program that `CreateProcess`es a child + uses handles. Verify the
     child launches and handles are closed correctly (no leak).
  2. Add two threads synchronized by a mutex/critical section + handle-based file I/O. Verify no data race
     on the shared resource and the file round-trips.
  3. Inspect via PowerShell + Process Explorer, then write `contrast.md` (Windows handles/objects vs Linux
     fd/`/proc`; `CreateProcess` vs `fork`/`exec`). Verify the inspection matches the code and the contrast
     is concrete.
- **Acceptance criteria**: process creation + synchronization + handle I/O work with no leak/race;
  PowerShell inspection matches the running program; the Windows-vs-Linux contrast is concrete.
- **Done bar**: runnable end-to-end (Windows) + observed via tooling + web-verified.

## Read more

**Books**

- **Windows Internals, Part 1**, 7th ed. — Pavel Yosifovich, Alex Ionescu, Mark E. Russinovich, David A. Solomon (2017). The definitive deep-dive into Windows architecture, processes, threads, and memory management.
- **Windows Internals, Part 2**, 7th ed. — Andrea Allievi, Alex Ionescu, Mark E. Russinovich, David A. Solomon (2021). Companion volume covering storage, I/O, networking, the boot process, and Windows management mechanisms.
- **Troubleshooting with the Windows Sysinternals Tools**, 2nd ed. — Mark Russinovich, Aaron Margosis (2016). The official field guide to the Sysinternals toolset for diagnosing real-world Windows problems.
- **Windows System Programming**, 4th ed. — Johnson M. Hart (2010). Long-running canonical reference for the Windows API at the systems-programming level (processes, threads, memory, sync, IPC).

**Papers & articles**

- **Sysinternals** — Mark Russinovich et al. (Microsoft). Official free toolkit and documentation; the de facto standard suite for Windows internals investigation and troubleshooting. <https://learn.microsoft.com/en-us/sysinternals/>

---

← Previous: [79 · Linux OS](./79-linux-os.md) · Next: [81 · System Programming](./81-system-programming.md) →

---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use these five sections in order. Answer from memory first; the goal is to reason about Windows resources, not to memorize spellings.

## 1. Recall Q&A

1. What is the difference between a Windows object and a handle? (co-04, co-05)
2. Why close both hProcess and hThread from PROCESS_INFORMATION? (co-06, co-07)
3. When should you choose a mutex instead of a critical section? (co-14, co-16)
4. What marks a file handle for overlapped I/O? (co-18, co-19)
5. Why is HANDLE equals fd an unsafe shortcut? (co-27)

<details><summary>Answer check</summary>

A handle is a caller-owned reference to an OS object. Close every successfully acquired handle. A mutex may cross process boundaries; a critical section is in-process only. Overlapped files use FILE_FLAG_OVERLAPPED, OVERLAPPED state, and a completion wait. A HANDLE can name many object types; an fd is not the Windows object model.

</details>

## 2. Applied Scenarios

- A child launches but the parent exits too early: name the process handle to wait on and the close order.
- Two threads increment one counter: describe one mutex solution and one critical-section solution.
- ReadFile returns before data is ready: identify the handle flag, OVERLAPPED, completion event, and wait.
- Registry inspection succeeds in PowerShell but C fails: check hive, access mask, and error code.

## 3. Code Katas

1. Create an auto-reset event, start a worker, wait, then close worker and event handles.
2. Reserve two pages with VirtualAlloc, commit one, then release the region.
3. Create a temporary file with FILE_FLAG_OVERLAPPED and wait for a short write.
4. Add a --child branch to a program, then prove every parent handle is closed.

## 4. Self-check Checklist

- [ ] I test each Win32 return value with its documented failure sentinel.
- [ ] I list every handle my function owns and close it exactly once.
- [ ] I can explain mutex versus critical-section scope.
- [ ] I can trace an overlapped operation to its completion event.
- [ ] I keep Windows handles separate from Linux fd and /proc terminology.

## 5. Explain Why

- Why can it be correct to close a process handle while its child is still running?
- Why is a critical section not a cross-process lock?
- Why do waitable objects give Windows APIs a uniform orchestration shape?
- Why does a fresh-image CreateProcess model change child setup?

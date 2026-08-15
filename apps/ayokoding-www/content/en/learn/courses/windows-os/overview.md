---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- **Prior topic**: [Just Enough C](../just-enough-c/learning/overview.md) supplies pointers, structs, functions, and return-value checks. This course does not reteach C syntax.
- **Tools and environment**: a Windows machine, PowerShell, and MSVC or MinGW that targets Windows. Task Manager is built in; Process Explorer is optional for handle inspection.
- **Assumed knowledge**: C pointers and structs, command-line execution, and the broad idea of processes, threads, memory, and files.

## Why this exists

Windows is an object-and-handle operating system. A program creates or opens an object, receives a handle, waits or performs I/O through it, and closes its own reference when it is finished. This course teaches that model through Win32 C and PowerShell observations.

> **Scope boundary — Windows OS vs. Linux OS.** This course owns **Windows-only internals and APIs**: user/kernel mode as surfaced by Win32, objects and handles, CreateProcess, the registry, Win32 synchronization, NTFS, overlapped I/O, and PowerShell inspection. [Linux OS](../linux-os/overview.md) owns Linux-family syscalls, file descriptors, /proc, the VFS, and fork/exec. Linux mechanisms appear here only in explicit contrast; this is not a Linux syscall or shell course.

## Learning route

The 78 independent examples start with Win32 calls and handle lifecycle, then add processes, threads, memory, synchronization, files, registry, and inspection. The advanced tier combines them in one small Windows-native program. Every C example is original and self-contained; no Linux environment or third-party C library is required.

## Concepts

### co-01 · user-kernel-mode

Applications run in user mode and request privileged work from kernel-mode components through APIs.

### co-02 · win32-api

The Win32 API is the C-facing user-mode surface used throughout this course.

### co-03 · subsystems

Win32 is a user-mode subsystem layered over the Windows kernel.

### co-04 · object-handle-model

Kernel resources are objects; a program usually refers to them through handles.

### co-05 · handle-lifecycle

CloseHandle releases the caller's reference; it does not necessarily destroy the object.

### co-06 · createprocess

CreateProcess starts a new process and its primary thread from a program image.

### co-07 · process-primary-thread

Every new process begins with one primary thread in PROCESS_INFORMATION.

### co-08 · createthread

CreateThread starts work inside the current process address space.

### co-09 · thread-scheduling

Windows schedules runnable threads preemptively; priority is a bias, not a guarantee.

### co-10 · virtualalloc

VirtualAlloc reserves, commits, and protects virtual address regions.

### co-11 · reserve-commit

Reservation selects address space; commitment makes pages accessible.

### co-12 · heaps

Private heaps are allocation domains for a process.

### co-13 · working-set

A working set is the subset of a process's recently used resident pages.

### co-14 · mutex

A mutex is a waitable mutual-exclusion object and may be named for cross-process use.

### co-15 · event

An event is a waitable signal with manual-reset or auto-reset behavior.

### co-16 · critical-section

A critical section is a lightweight in-process lock, not a kernel object.

### co-17 · wait-functions

Wait functions observe process, thread, mutex, and event completion uniformly.

### co-18 · createfile

CreateFile opens a file or device and reports failure with INVALID_HANDLE_VALUE.

### co-19 · sync-async-io

Overlapped I/O uses FILE_FLAG_OVERLAPPED, OVERLAPPED state, and completion observation.

### co-20 · ntfs

NTFS adds Windows file features such as alternate data streams.

### co-21 · registry

The registry is a hierarchical configuration database of keys and values.

### co-22 · registry-api

Registry APIs open and query HKEY values rather than file handles.

### co-23 · powershell-getprocess

Get-Process supplies Windows process observations from PowerShell.

### co-24 · powershell-getservice

Get-Service supplies Windows service observations from PowerShell.

### co-25 · process-explorer

Process Explorer can show a process's handles and loaded modules.

### co-26 · task-manager

Task Manager gives the built-in summary of processes and resource activity.

### co-27 · handle-vs-fd

A HANDLE may name many Windows object types; a Linux file descriptor is file-oriented.

### co-28 · createprocess-vs-fork

CreateProcess starts a new image; fork duplicates state before exec replaces it.

### co-29 · object-manager-vs-vfs

The Object Manager names broad Windows object types; the Linux VFS focuses on filesystems.

### co-30 · os-theory

Operating-system concepts recur across families, but APIs and resource models differ.

## Examples by Level

The [Learning overview](./learning/overview.md) links all 78 contiguous examples by level and states their Windows-only run instructions.

## Primary references

- [Windows API reference](https://learn.microsoft.com/windows/win32/apiindex/windows-api-list)
- [CreateProcess](https://learn.microsoft.com/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessa)
- [CloseHandle](https://learn.microsoft.com/windows/win32/api/handleapi/nf-handleapi-closehandle)
- [Synchronous and asynchronous I/O](https://learn.microsoft.com/windows/win32/fileio/synchronous-and-asynchronous-i-o)

Next: [Learning overview](./learning/overview.md) →

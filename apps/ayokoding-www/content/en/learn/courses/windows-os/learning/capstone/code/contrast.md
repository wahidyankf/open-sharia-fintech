# Windows and Linux: two deliberately different process-resource models

This Windows-only course uses objects and handles. CreateEvent, CreateMutex, CreateFile, a process,
and a thread are distinct Windows object kinds; an owning process refers to an object through a
handle in its handle table. CloseHandle releases that process reference. It does not mean “kill the
process” or “destroy the object immediately”: other references may still exist.

Linux uses file descriptors as small integers for its file-oriented interfaces and exposes process
observation through facilities such as /proc. A file descriptor is useful for files, pipes, sockets,
and devices, but it is not a name for the full Windows Object Manager model. The two ideas solve
related resource-management problems; treating a HANDLE as merely an fd loses the fact that Windows
waitable objects include processes, threads, events, and mutexes.

Process creation is similarly distinct. The capstone calls CreateProcess with a program image and
command line, receiving the new process and primary-thread handles in PROCESS_INFORMATION. The child
begins by executing that fresh image main function. A typical POSIX sequence is fork, which
duplicates the calling process, followed by exec, which replaces the duplicated image. Neither
mechanism is an alias for the other. This course invokes no Linux process API; Linux OS owns fork,
exec, fd, /proc, syscall, and VFS details.

The useful comparison is conceptual: both families have processes, files, waiting, and concurrent
work. Correct code follows platform-specific lifetime and failure rules at the native boundary.

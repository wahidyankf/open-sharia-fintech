#define WIN32_LEAN_AND_MEAN
#include <stdio.h>
#include <string.h>
#include <windows.h>

static HANDLE g_mutex;
static CRITICAL_SECTION g_counter_lock;
static LONG g_counter;

static DWORD WINAPI increment_counter(void *unused) {
  (void)unused;
  // => A mutex can coordinate access across Windows processes.
  if (WaitForSingleObject(g_mutex, INFINITE) != WAIT_OBJECT_0)
    return 1;
  // => A critical section is fast in-process protection for the shared counter.
  EnterCriticalSection(&g_counter_lock);
  ++g_counter;
  LeaveCriticalSection(&g_counter_lock);
  ReleaseMutex(g_mutex);
  // => Both synchronization mechanisms release before the worker exits.
  return 0;
}

static int write_overlapped_file(void) {
  char folder[MAX_PATH], temporary[MAX_PATH];
  OVERLAPPED operation = {0};
  DWORD written = 0;
  const char payload[] = "Windows OS capstone\r\n";

  if (!GetTempPathA(MAX_PATH, folder) ||
      !GetTempFileNameA(folder, "wos", 0, temporary))
    return 1;
  // => A temporary name keeps the example self-contained.
  HANDLE file = CreateFileA(temporary, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS,
                            FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, NULL);
  // => FILE_FLAG_OVERLAPPED requests asynchronous handle-based I/O.
  if (file == INVALID_HANDLE_VALUE)
    return 1;
  operation.hEvent = CreateEventA(NULL, TRUE, FALSE, NULL);
  // => The event is the completion signal associated with this OVERLAPPED
  // operation.
  if (operation.hEvent == NULL) {
    CloseHandle(file);
    DeleteFileA(temporary);
    return 1;
  }

  BOOL started =
      WriteFile(file, payload, (DWORD)strlen(payload), NULL, &operation);
  if (!started && GetLastError() != ERROR_IO_PENDING) {
    CloseHandle(operation.hEvent);
    CloseHandle(file);
    DeleteFileA(temporary);
    return 1;
  }
  // => ERROR_IO_PENDING is normal; wait before asking for final byte count.
  if (WaitForSingleObject(operation.hEvent, INFINITE) != WAIT_OBJECT_0 ||
      !GetOverlappedResult(file, &operation, &written, FALSE)) {
    CloseHandle(operation.hEvent);
    CloseHandle(file);
    DeleteFileA(temporary);
    return 1;
  }
  printf("overlapped write: %lu bytes\n", written);
  CloseHandle(operation.hEvent);
  CloseHandle(file);
  // => Both I/O handles close only after the operation completes.
  DeleteFileA(temporary);
  return 0;
}

int main(int argc, char **argv) {
  if (argc == 2 && strcmp(argv[1], "--child") == 0) {
    // => The child path is a fresh image launched by CreateProcess.
    puts("child started");
    return 0;
  }
  char executable[MAX_PATH], command[MAX_PATH + 16];
  STARTUPINFOA startup = {.cb = sizeof(startup)};
  PROCESS_INFORMATION child = {0};
  if (!GetModuleFileNameA(NULL, executable, MAX_PATH))
    return 1;
  snprintf(command, sizeof(command), "\"%s\" --child", executable);
  // => CreateProcess may modify its mutable command-line buffer.
  if (!CreateProcessA(NULL, command, NULL, NULL, FALSE, 0, NULL, NULL, &startup,
                      &child))
    return 1;

  g_mutex = CreateMutexA(NULL, FALSE, NULL);
  if (g_mutex == NULL) {
    CloseHandle(child.hThread);
    CloseHandle(child.hProcess);
    return 1;
  }
  InitializeCriticalSection(&g_counter_lock);
  HANDLE workers[2] = {CreateThread(NULL, 0, increment_counter, NULL, 0, NULL),
                       CreateThread(NULL, 0, increment_counter, NULL, 0, NULL)};
  if (workers[0] == NULL || workers[1] == NULL)
    return 1;
  // => Each worker owns no external state beyond the synchronization objects.
  WaitForMultipleObjects(2, workers, TRUE, INFINITE);
  WaitForSingleObject(child.hProcess, INFINITE);
  printf("workers completed: counter=%ld\n", g_counter);

  int io_result = write_overlapped_file();
  CloseHandle(workers[0]);
  CloseHandle(workers[1]);
  CloseHandle(child.hThread);
  CloseHandle(child.hProcess);
  CloseHandle(g_mutex);
  DeleteCriticalSection(&g_counter_lock);
  // => The parent closes every acquired handle, including PROCESS_INFORMATION
  // handles.
  return (g_counter == 2 && io_result == 0) ? 0 : 1;
}

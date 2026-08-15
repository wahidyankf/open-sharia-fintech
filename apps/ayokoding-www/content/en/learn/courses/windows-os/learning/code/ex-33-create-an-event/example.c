#define WIN32_LEAN_AND_MEAN
#include <stdio.h>
#include <windows.h>

int main(void) {
  // => This standalone example stays inside the Windows Win32 API surface.
  HANDLE marker = CreateEventA(NULL, TRUE, FALSE, NULL);
  // => CreateEvent returns an owned HANDLE for a waitable kernel object.
  if (marker == NULL) {
    // => A failed call supplies a Windows error code through GetLastError.
    return (int)GetLastError();
  }
  printf("Example 33: Create an Event; pid=%lu\n", GetCurrentProcessId());
  // => The output identifies the process that owns this handle table entry.
  SetEvent(marker);
  // => Signaling makes the event immediately observable by a waiter.
  DWORD state = WaitForSingleObject(marker, 0);
  // => WaitForSingleObject provides one uniform observation API for waitable
  // objects.
  CloseHandle(marker);
  // => Closing releases this program's reference and prevents a handle leak.
  return state == WAIT_OBJECT_0 ? 0 : 1;
}

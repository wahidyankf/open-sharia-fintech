#define WIN32_LEAN_AND_MEAN
#include <stdio.h>
#include <windows.h>

int main(void) {
  // => This console program runs in the Win32 user-mode subsystem.
  HANDLE marker = CreateEventA(NULL, TRUE, FALSE, NULL);
  // => An event is a kernel object; marker is this process's HANDLE reference.
  if (marker == NULL) {
    // => GetLastError identifies why the Windows call failed.
    return (int)GetLastError();
  }
  printf("Example 20: WriteFile; pid=%lu\n", GetCurrentProcessId());
  // => GetCurrentProcessId observes the caller without creating another
  // resource.
  SetEvent(marker);
  // => The event becomes signaled before this program checks it.
  DWORD state = WaitForSingleObject(marker, 0);
  // => A zero timeout turns waiting into a non-blocking state observation.
  CloseHandle(marker);
  // => CloseHandle releases this process's reference on every success path.
  return state == WAIT_OBJECT_0 ? 0 : 1;
}

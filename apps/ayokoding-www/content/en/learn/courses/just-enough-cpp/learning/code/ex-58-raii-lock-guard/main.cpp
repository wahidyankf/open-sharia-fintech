// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
#include <mutex>
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
int main() {
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
  std::mutex mutex;
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
  { std::lock_guard<std::mutex> lock(mutex); std::cout << "locked\n"; }
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
  std::cout << "released\n";
// => raii-lock-guard: this line establishes the runnable C++ state or behavior.
}

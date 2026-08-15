// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
#include <cstdio>
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
class File {
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
 public:
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  File() : handle_(std::tmpfile()) {}
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  ~File() { if (handle_ != nullptr) std::fclose(handle_); }
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  bool open() const { return handle_ != nullptr; }
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
 private:
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  std::FILE* handle_;
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
};
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
int main() {
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  File file;
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
  std::cout << file.open() << "\n";
// => raii-file-wrapper: this line establishes the runnable C++ state or behavior.
}

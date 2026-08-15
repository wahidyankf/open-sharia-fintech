// => rule-of-three: this line establishes the runnable C++ state or behavior.
#include <cstring>
// => rule-of-three: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => rule-of-three: this line establishes the runnable C++ state or behavior.
#include <utility>
// => rule-of-three: this line establishes the runnable C++ state or behavior.
class Text {
// => rule-of-three: this line establishes the runnable C++ state or behavior.
 public:
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  explicit Text(const char* source) : data_(new char[std::strlen(source) + 1]) { std::strcpy(data_, source); }
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  ~Text() { delete[] data_; }
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  Text(const Text& other) : Text(other.data_) {}
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  Text& operator=(const Text& other) { if (this != &other) { Text copy(other); std::swap(data_, copy.data_); } return *this; }
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  const char* get() const { return data_; }
// => rule-of-three: this line establishes the runnable C++ state or behavior.
 private:
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  char* data_;
// => rule-of-three: this line establishes the runnable C++ state or behavior.
};
// => rule-of-three: this line establishes the runnable C++ state or behavior.
int main() {
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  Text first("Ada"); Text second = first;
// => rule-of-three: this line establishes the runnable C++ state or behavior.
  std::cout << second.get() << "\n";
// => rule-of-three: this line establishes the runnable C++ state or behavior.
}

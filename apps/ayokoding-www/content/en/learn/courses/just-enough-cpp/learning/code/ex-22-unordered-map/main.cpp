// => unordered-map: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => unordered-map: this line establishes the runnable C++ state or behavior.
#include <string>
// => unordered-map: this line establishes the runnable C++ state or behavior.
#include <unordered_map>
// => unordered-map: this line establishes the runnable C++ state or behavior.
int main() {
// => unordered-map: this line establishes the runnable C++ state or behavior.
  std::unordered_map<std::string, int> counts{{"ok", 2}};
// => unordered-map: this line establishes the runnable C++ state or behavior.
  std::cout << counts.count("ok") << "\n";
// => unordered-map: this line establishes the runnable C++ state or behavior.
}

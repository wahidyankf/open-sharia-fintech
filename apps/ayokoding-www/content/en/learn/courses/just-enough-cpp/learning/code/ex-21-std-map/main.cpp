// => std-map: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => std-map: this line establishes the runnable C++ state or behavior.
#include <map>
// => std-map: this line establishes the runnable C++ state or behavior.
#include <string>
// => std-map: this line establishes the runnable C++ state or behavior.
int main() {
// => std-map: this line establishes the runnable C++ state or behavior.
  std::map<std::string, int> scores{{"Ada", 10}, {"Lin", 9}};
// => std-map: this line establishes the runnable C++ state or behavior.
  std::cout << scores.begin()->first << ":" << scores.at("Ada") << "\n";
// => std-map: this line establishes the runnable C++ state or behavior.
}

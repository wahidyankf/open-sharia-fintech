// => scoped-enum: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => scoped-enum: this line establishes the runnable C++ state or behavior.
enum class Level { info, warning };
// => scoped-enum: this line establishes the runnable C++ state or behavior.
int main() {
// => scoped-enum: this line establishes the runnable C++ state or behavior.
  const Level level = Level::warning;
// => scoped-enum: this line establishes the runnable C++ state or behavior.
  std::cout << (level == Level::warning) << "\n";
// => scoped-enum: this line establishes the runnable C++ state or behavior.
}

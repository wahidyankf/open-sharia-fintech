// => Imports the public behavior under test.
#include "task.hpp"
// => Provides a minimal failure return path.
int main() {
  // => Keeps this assertion dependency-free and suitable for CTest.
  return summarize({"write", "test"}) == "tasks:write,test" ? 0 : 1;
}

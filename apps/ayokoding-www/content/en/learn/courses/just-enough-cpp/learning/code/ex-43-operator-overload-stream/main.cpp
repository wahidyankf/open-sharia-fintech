// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
struct Point { int x; int y; };
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
std::ostream& operator<<(std::ostream& out, const Point& point) {
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
  return out << "(" << point.x << "," << point.y << ")";
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
}
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
int main() {
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
  std::cout << Point{2, 3} << "\n";
// => operator-overload-stream: this line establishes the runnable C++ state or behavior.
}

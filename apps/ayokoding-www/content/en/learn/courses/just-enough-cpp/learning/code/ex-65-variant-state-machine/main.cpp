// => variant-state-machine: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
#include <type_traits>
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
#include <variant>
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
struct Idle {};
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
struct Running { int progress; };
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
int main() {
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
  std::variant<Idle, Running> state = Running{50};
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
  std::visit([](const auto& current) { if constexpr (std::is_same_v<std::decay_t<decltype(current)>, Running>) std::cout << current.progress << "\n"; }, state);
// => variant-state-machine: this line establishes the runnable C++ state or behavior.
}

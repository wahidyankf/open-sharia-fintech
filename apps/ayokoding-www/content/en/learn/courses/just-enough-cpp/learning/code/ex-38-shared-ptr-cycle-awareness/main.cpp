// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
#include <memory>
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
struct Parent;
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
struct Child { std::shared_ptr<Parent> parent; };
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
struct Parent { std::weak_ptr<Child> child; };
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
int main() {
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
  auto parent = std::make_shared<Parent>();
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
  auto child = std::make_shared<Child>();
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
  parent->child = child;
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
  child->parent = parent;
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
  std::cout << parent.use_count() << ":" << child.use_count() << "\n";
// => shared-ptr-cycle-awareness: this line establishes the runnable C++ state or behavior.
}

// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
#include <memory>
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
#include <string>
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
struct Node {
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
  std::string name;
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
  std::unique_ptr<Node> child;
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
};
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
int main() {
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
  auto root = std::make_unique<Node>(Node{"root", nullptr});
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
  root->child = std::make_unique<Node>(Node{"leaf", nullptr});
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
  std::cout << root->child->name << "\n";
// => smart-pointer-tree: this line establishes the runnable C++ state or behavior.
}

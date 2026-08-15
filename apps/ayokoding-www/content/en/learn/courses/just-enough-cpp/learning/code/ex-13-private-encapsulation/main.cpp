// => private-encapsulation: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
class Account {
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
 public:
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
  int balance() const { return balance_; }
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
 private:
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
  int balance_ = 50;
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
};
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
int main() {
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
  Account account;
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
  std::cout << account.balance() << "\n";
// => private-encapsulation: this line establishes the runnable C++ state or behavior.
}

// => polymorphic-container: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
#include <memory>
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
#include <vector>
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
struct Job {
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  virtual ~Job() = default;
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  virtual int run() const = 0;
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
};
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
struct FixedJob : Job {
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  int run() const override { return 5; }
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
};
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
int main() {
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  std::vector<std::unique_ptr<Job>> jobs;
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  jobs.push_back(std::make_unique<FixedJob>());
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
  std::cout << jobs.front()->run() << "\n";
// => polymorphic-container: this line establishes the runnable C++ state or behavior.
}

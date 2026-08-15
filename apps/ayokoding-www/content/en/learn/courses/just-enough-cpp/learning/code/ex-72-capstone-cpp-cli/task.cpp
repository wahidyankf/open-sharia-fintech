// => Imports the capstone interface.
#include "task.hpp"
// => Provides algorithms, ownership, and error types used by the implementation.
#include <algorithm>
#include <memory>
#include <numeric>
#include <stdexcept>
#include <utility>
// => Turns a value into a one-item owned string resource.
template <typename T>
std::unique_ptr<T> owned(T value) { return std::make_unique<T>(std::move(value)); }
// => Implements the header contract with STL algorithms and a lambda.
std::string summarize(const std::vector<std::string>& tasks) {
  // => Rejects invalid domain input through an exception.
  if (tasks.empty()) throw std::invalid_argument("at least one task is required");
  // => Owns a transformed copy under RAII.
  auto joined = owned(std::accumulate(tasks.begin(), tasks.end(), std::string{}, [](std::string text, const std::string& task) {
    return text.empty() ? task : text + "," + task;
  }));
  // => Returns a value after the owned temporary has done its job.
  return "tasks:" + *joined;
}

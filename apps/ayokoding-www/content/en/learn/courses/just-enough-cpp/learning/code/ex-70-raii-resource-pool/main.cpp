// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
#include <iostream>
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
class Pool {
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
 public:
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  class Lease {
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
   public:
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
    explicit Lease(Pool& pool) : pool_(pool) { ++pool_.in_use_; }
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
    ~Lease() { --pool_.in_use_; }
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
   private:
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
    Pool& pool_;
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  };
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  int in_use() const { return in_use_; }
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
 private:
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  int in_use_ = 0;
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
};
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
int main() {
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  Pool pool; { Pool::Lease lease(pool); std::cout << pool.in_use() << "\n"; }
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
  std::cout << pool.in_use() << "\n";
// => raii-resource-pool: this line establishes the runnable C++ state or behavior.
}

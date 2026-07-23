// Example 51: Structural Interface Match -- no `implements` keyword needed at all.
interface Greeter {
  greet(): string; // => any object with a matching greet() method satisfies this
}

// => plain: has NO "implements Greeter" clause, yet it satisfies Greeter by shape alone
const plain = {
  greet(): string {
    return "hi";
  },
};

function useGreeter(g: Greeter): string {
  return g.greet();
}

console.log(useGreeter(plain)); // => Output: hi

// Example 16: Interface Declaration -- `interface` declares a named object contract.
interface User {
  id: number; // => every User must have a numeric id
  name: string; // => and a string name
}

const alice: User = { id: 1, name: "Alice" }; // => a conforming object satisfies User
console.log(alice); // => Output: { id: 1, name: 'Alice' }

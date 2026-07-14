// Example 63: Type-Only Import -- erased completely at compile time, no runtime cost.
import type { User } from "./types"; // => `import type` is GUARANTEED to disappear from output JS

const user: User = { id: 1, name: "Ada" }; // => User is used only as a type annotation here
console.log(user); // => Output: { id: 1, name: 'Ada' }

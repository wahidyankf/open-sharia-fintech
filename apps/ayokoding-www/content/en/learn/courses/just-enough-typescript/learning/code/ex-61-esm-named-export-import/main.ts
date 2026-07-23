// Example 61: ESM Named Export Import -- imports square from the sibling util.ts.
import { square } from "./util"; // => a named import, matching util.ts's named export

console.log(square(6)); // => Output: 36

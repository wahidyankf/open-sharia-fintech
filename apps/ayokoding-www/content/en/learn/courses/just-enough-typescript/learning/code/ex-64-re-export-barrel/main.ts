// Example 64: Re-Export Barrel -- one import path resolves BOTH sibling functions.
import { addOne, double } from "./index"; // => a single import path, two different source modules

console.log(addOne(1), double(4)); // => Output: 2 8

// Example 62: ESM Default Export -- the import binding's name is chosen locally.
import shout from "./util"; // => no braces -- binds the default export under any local name

console.log(shout("hi")); // => Output: HI!

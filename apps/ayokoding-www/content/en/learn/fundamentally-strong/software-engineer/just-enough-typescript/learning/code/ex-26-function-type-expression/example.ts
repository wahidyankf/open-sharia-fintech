// Example 26: Function Type Expression -- a standalone type for "a function shaped like this".
let format: (n: number) => string; // => format must be a function: takes number, returns string

format = (n) => `#${n}`; // => this arrow matches the (n: number) => string shape exactly
console.log(format(7)); // => Output: #7

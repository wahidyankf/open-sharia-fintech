// Example 26 (invalid): this arrow returns a number, not the required string.
let format: (n: number) => string;

format = (n) => n * 2; // => TYPE ERROR: returns number, but the type expression requires string
console.log(format(7));

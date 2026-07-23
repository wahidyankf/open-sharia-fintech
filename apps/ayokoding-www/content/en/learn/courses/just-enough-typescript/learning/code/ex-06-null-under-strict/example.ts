// Example 6: Null Under Strict -- a union type explicitly allows null.
let x: string | null = null; // => x is null (type: string | null) -- the union permits it
console.log(x); // => Output: null

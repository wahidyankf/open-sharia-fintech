// Example 6 (invalid): a bare string binding rejects null under strict mode.
let s: string = null; // => TYPE ERROR: null is not assignable to string under strict
console.log(s);

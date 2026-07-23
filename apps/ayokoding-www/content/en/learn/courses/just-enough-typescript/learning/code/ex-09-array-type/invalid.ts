// Example 9 (invalid): pushing a string onto a number[] fails.
const xs: number[] = [1, 2, 3];
xs.push("bad"); // => TYPE ERROR: a string argument is not assignable to number

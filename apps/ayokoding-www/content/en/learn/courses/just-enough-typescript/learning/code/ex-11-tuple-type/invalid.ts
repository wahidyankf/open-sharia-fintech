// Example 11 (invalid): a third element does not fit a two-element tuple type.
const p: [number, number] = [1, 2, 3]; // => TYPE ERROR: source has too many elements
console.log(p);

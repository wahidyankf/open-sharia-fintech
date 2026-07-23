// Example 12 (invalid): a named 3-tuple still rejects the wrong number of elements.
const rgb: [r: number, g: number, b: number] = [255, 0]; // => TYPE ERROR: missing element 'b'
console.log(rgb);

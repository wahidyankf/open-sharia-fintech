// Example 10 (invalid): readonly number[] has no push method at all.
const xs: readonly number[] = [1, 2, 3];
xs.push(4); // => TYPE ERROR: Property 'push' does not exist on type 'readonly number[]'

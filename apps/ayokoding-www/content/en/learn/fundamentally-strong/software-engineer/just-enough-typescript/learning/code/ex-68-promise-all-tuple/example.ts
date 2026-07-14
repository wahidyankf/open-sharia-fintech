// Example 68: Promise All Tuple -- Promise.all preserves each promise's OWN resolved type.
async function run(): Promise<void> {
  const [n, s] = await Promise.all([
    Promise.resolve(42), // => resolves to number
    Promise.resolve("hi"), // => resolves to string
  ]); // => the destructured result keeps [number, string], not (number | string)[]
  console.log(n, s); // => Output: 42 hi
}

run();

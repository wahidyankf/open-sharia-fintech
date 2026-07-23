// Example 66: Async Await Typed -- await unwraps Promise<number> to plain number.
function fetchN(): Promise<number> {
  return Promise.resolve(42); // => declared return type is Promise<number>, matching the signature
}

async function run(): Promise<void> {
  const n = await fetchN(); // => n's type is number, not Promise<number>
  console.log(n); // => Output: 42
}

run(); // => kicks off the async function -- output appears once the awaited promise resolves

// Example 65: Typed Promise -- Promise<number> documents what the eventual value will be.
function fetchN(): Promise<number> {
  return Promise.resolve(42); // => resolves immediately with a number
}

fetchN().then((n) => {
  // => n's type is inferred as number, from Promise<number>'s type parameter
  console.log(n); // => Output: 42
});

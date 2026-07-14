// Example 67: Async Error Typed -- a caught error's type is unknown under strict.
function risky(): Promise<number> {
  return Promise.reject(new Error("boom")); // => a promise that always rejects
}

async function run(): Promise<void> {
  try {
    await risky();
  } catch (err) {
    // => err's type is unknown -- must be narrowed before it can be used
    if (err instanceof Error) {
      console.log(err.message); // => .message is safe only after narrowing to Error
    }
  }
}

run(); // => Output: boom

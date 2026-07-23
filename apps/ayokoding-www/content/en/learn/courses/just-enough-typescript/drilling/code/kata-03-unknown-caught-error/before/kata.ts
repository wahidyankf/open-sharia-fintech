// Kata 3 (before): a caught error's type is unknown under strict -- .message fails to compile.
function risky(): void {
  throw new Error("network timeout");
}

function run(): void {
  try {
    risky();
  } catch (err) {
    console.log(err.message);
  }
}

run();

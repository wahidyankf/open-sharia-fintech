// Kata 3 (after): narrow err with instanceof Error before reading .message.
function risky(): void {
  throw new Error("network timeout");
}

function run(): void {
  try {
    risky();
  } catch (err) {
    if (err instanceof Error) {
      console.log(err.message);
    }
  }
}

run();

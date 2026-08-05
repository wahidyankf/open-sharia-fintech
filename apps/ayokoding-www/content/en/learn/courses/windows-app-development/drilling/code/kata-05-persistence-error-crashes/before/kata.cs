// Kata 5 before: The before version lets storage failure escape; the after version maps it to recoverable view state.
// => Run this file and identify why the behavior violates the UI contract.
throw new IOException("disk unavailable");

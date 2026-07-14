// Example 32: Narrow instanceof -- instanceof checks a value's runtime constructor.
function describeWhen(value: Date | string): string {
  if (value instanceof Date) {
    // => inside this branch, value is narrowed to Date
    return value.getFullYear().toString(); // => .getFullYear() only exists on Date
  }
  return value; // => here, value is narrowed to string
}

console.log(describeWhen(new Date("2026-01-01"))); // => Output: 2026
console.log(describeWhen("today")); // => Output: today

// Example 28: Run Typed Script tsx -- several typed functions, run end to end with tsx.
function celsiusToFahrenheit(c: number): number {
  return (c * 9) / 5 + 32; // => the standard C-to-F conversion formula
}

function describeTemp(f: number): string {
  // => a plain if/else chain -- categorizes a Fahrenheit reading
  if (f < 32) return "freezing"; // => below the freezing point of water
  if (f < 70) return "cool"; // => between freezing and 70
  return "warm"; // => 70 and above
}

const readings: number[] = [0, 20, 37]; // => three Celsius readings to process
for (const c of readings) {
  // => loops over each reading, converting and describing it
  const f = celsiusToFahrenheit(c); // => f is the Fahrenheit equivalent of c
  console.log(`${c}C -> ${f}F (${describeTemp(f)})`);
  // => Output: one line per reading
}

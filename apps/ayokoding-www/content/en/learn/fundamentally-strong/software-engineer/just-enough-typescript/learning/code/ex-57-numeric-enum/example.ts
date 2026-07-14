// Example 57: Numeric Enum -- enum members auto-number from 0, with a runtime reverse map.
enum Color {
  Red, // => Color.Red is 0 (the first member, unless given an explicit value)
  Green, // => Color.Green is 1
  Blue, // => Color.Blue is 2
}

console.log(Color.Red === 0); // => Output: true
console.log(Color[0]); // => reverse mapping: numeric value 0 back to its name -- Output: Red

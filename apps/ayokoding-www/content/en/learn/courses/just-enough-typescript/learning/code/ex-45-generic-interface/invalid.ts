// Example 45 (invalid): Box<number> requires value to be a number, not a string.
interface Box<T> {
  value: T;
}

const numberBox: Box<number> = { value: "oops" }; // => TYPE ERROR: string is not number
console.log(numberBox);

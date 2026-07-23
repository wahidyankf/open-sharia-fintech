// Example 45: Generic Interface -- Box<T> stores exactly one value of type T.
interface Box<T> {
  value: T; // => value's type is whatever T is instantiated with
}

const numberBox: Box<number> = { value: 42 }; // => T=number -- value must be a number
console.log(numberBox); // => Output: { value: 42 }

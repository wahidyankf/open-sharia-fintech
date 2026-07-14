// Example 9: Array Type -- T[] types a homogeneous, mutable list.
const xs: number[] = [1, 2, 3]; // => xs is [1, 2, 3] (type: number[])
xs.push(4); // => push accepts only number -- mutates xs in place
console.log(xs); // => Output: [ 1, 2, 3, 4 ]

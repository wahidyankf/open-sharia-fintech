// Example 72: Utility Record -- Record<K, V> is a shorthand for an index signature.
type Scores = Record<string, number>; // => equivalent to { [key: string]: number }

const scores: Scores = { alice: 90, bob: 85 }; // => arbitrary string keys, all numeric values
console.log(scores.alice); // => Output: 90

// Example 60: Index Signature -- [k: string]: number types an open-ended set of keys.
type Dict = { [key: string]: number }; // => ANY string key maps to a number value

const inventory: Dict = { apples: 3, bananas: 5 }; // => arbitrary keys, all numeric values
console.log(inventory["apples"]); // => Output: 3
console.log(inventory.bananas); // => Output: 5

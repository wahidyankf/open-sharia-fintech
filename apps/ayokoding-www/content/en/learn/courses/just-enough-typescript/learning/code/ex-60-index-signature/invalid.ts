// Example 60 (invalid): a Dict value must be number -- a string value violates the signature.
type Dict = { [key: string]: number };

const inventory: Dict = { apples: 3, bananas: "five" }; // => TYPE ERROR: string is not number
console.log(inventory);

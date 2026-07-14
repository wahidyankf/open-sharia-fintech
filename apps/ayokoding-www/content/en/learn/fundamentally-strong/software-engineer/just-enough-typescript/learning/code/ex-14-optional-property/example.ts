// Example 14: Optional Property -- age? marks the field as not required.
function describe(person: { name: string; age?: number }): string {
  // => age?: number means age can be a number OR be entirely omitted
  return person.age === undefined
    ? person.name // => no age supplied -- just the name
    : `${person.name} (${person.age})`; // => age supplied -- include it
}

console.log(describe({ name: "Ada" })); // => Output: Ada
console.log(describe({ name: "Grace", age: 85 })); // => Output: Grace (85)

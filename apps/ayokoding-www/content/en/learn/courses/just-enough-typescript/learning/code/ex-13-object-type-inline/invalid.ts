// Example 13 (invalid): calling greet without the required age field.
function greet(person: { name: string; age: number }): string {
  return `${person.name} is ${person.age}`;
}

console.log(greet({ name: "Ada" })); // => TYPE ERROR: property 'age' is missing

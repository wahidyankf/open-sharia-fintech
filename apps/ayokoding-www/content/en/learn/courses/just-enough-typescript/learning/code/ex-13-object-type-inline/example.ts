// Example 13: Object Type Inline -- an inline object type annotates a parameter's shape.
function greet(person: { name: string; age: number }): string {
  // => person must have exactly a name (string) and age (number) field
  return `${person.name} is ${person.age}`; // => builds and returns a template string
}

console.log(greet({ name: "Ada", age: 36 })); // => Output: Ada is 36

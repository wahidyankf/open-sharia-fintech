// Example 52: Intersection Type -- Staff must satisfy BOTH Person AND Employee at once.
type Person = { name: string };
type Employee = { employeeId: number };
type Staff = Person & Employee; // => a Staff value needs every field from both types

const worker: Staff = { name: "Ada", employeeId: 7 }; // => both required fields present
console.log(worker); // => Output: { name: 'Ada', employeeId: 7 }

// Example 31: Narrow In Operator -- the `in` operator checks for a property's presence.
type Guest = { name: string };
type Staff = { name: string; role: string };

function label(person: Guest | Staff): string {
  if ("role" in person) {
    // => inside this branch, person is narrowed to Staff -- the only variant with 'role'
    return `${person.name} (${person.role})`; // => .role is safe to read here
  }
  return person.name; // => here, person is narrowed to Guest
}

console.log(label({ name: "Ada" })); // => Output: Ada
console.log(label({ name: "Grace", role: "admin" })); // => Output: Grace (admin)

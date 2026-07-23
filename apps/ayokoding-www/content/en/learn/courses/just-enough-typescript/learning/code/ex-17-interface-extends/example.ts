// Example 17: Interface Extends -- Admin inherits every User field, plus its own.
interface User {
  id: number; // => required on User AND on anything that extends User
  name: string; // => same rule -- inherited automatically, no re-declaration needed
}

interface Admin extends User {
  // => compile-time only -- no runtime class hierarchy is created
  role: string; // => Admin requires id, name (inherited), AND role
}

const root: Admin = { id: 1, name: "Root", role: "superuser" }; // => all three fields present
console.log(root); // => Output: { id: 1, name: 'Root', role: 'superuser' }

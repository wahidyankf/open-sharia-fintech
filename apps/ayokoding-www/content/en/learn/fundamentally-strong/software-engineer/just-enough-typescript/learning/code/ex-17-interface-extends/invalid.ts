// Example 17 (invalid): Admin is missing role, its own required field.
interface User {
  id: number;
  name: string;
}

interface Admin extends User {
  role: string; // => still required on Admin -- root below omits it, which is why this fails
}

const root: Admin = { id: 1, name: "Root" }; // => TYPE ERROR: 'role' is missing
console.log(root); // => never reached -- tsc rejects this file before runtime

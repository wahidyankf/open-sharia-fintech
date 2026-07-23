// Kata 5 (after): a real null check replaces the assertion -- no crash, no lie to the compiler.
function findUser(id: number): { name: string } | null {
  return id === 1 ? { name: "Ada" } : null;
}

const user = findUser(2);
if (user !== null) {
  console.log(user.name);
} else {
  console.log("user not found");
}

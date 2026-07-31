import { writeFileSync } from "node:fs";

writeFileSync("dist.txt", "built locally\\n");
console.log("built dist.txt");

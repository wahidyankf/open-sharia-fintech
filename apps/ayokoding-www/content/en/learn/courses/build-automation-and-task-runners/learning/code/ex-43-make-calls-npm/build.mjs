import { writeFileSync } from "node:fs";

writeFileSync("dist.txt", "web build\\n");
console.log("built dist.txt");

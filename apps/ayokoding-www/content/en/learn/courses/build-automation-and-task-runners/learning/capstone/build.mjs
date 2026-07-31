import { writeFileSync } from "node:fs";

writeFileSync("dist.txt", "JavaScript build artifact\n");
console.log("built dist.txt");

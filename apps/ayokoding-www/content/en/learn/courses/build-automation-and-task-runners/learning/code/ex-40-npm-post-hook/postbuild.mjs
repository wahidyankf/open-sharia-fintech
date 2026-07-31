import { appendFileSync } from "node:fs";

appendFileSync("order.txt", "postbuild\\n");

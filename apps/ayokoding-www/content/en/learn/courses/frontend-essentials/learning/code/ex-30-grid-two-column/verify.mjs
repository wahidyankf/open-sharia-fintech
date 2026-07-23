// ex-30: verify two children land in two separate grid columns (co-10).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const boxA = await page.locator("#a").boundingBox();
const boxB = await page.locator("#b").boundingBox();
console.log("a.x:", boxA.x, "a.width:", boxA.width, "b.x:", boxB.x);
if (boxA.y !== boxB.y) throw new Error("expected both cells on the same grid row");
if (boxB.x <= boxA.x) throw new Error("expected b to be to the right of a, in a separate column");
if (Math.abs(boxA.width - 200) > 1) throw new Error(`expected each 1fr column to be 200px, got ${boxA.width}`);
console.log("PASS: the two children landed in two separate, equal-width grid columns");

await browser.close();

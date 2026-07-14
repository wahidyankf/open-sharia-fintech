// ex-16: verify offsetParent becomes null once display: none is toggled on (co-08).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const before = await page.locator("#panel").evaluate((el) => el.offsetParent !== null);
await page.locator("#panel").evaluate((el) => el.classList.add("hidden"));
const after = await page.locator("#panel").evaluate((el) => el.offsetParent);
console.log("offsetParent set before hiding:", before, "offsetParent after display:none:", after);

if (!before) throw new Error("panel should have an offsetParent before hiding");
if (after !== null) throw new Error("offsetParent should become null once display:none applies");
console.log("PASS: display:none removed the element from layout (offsetParent === null)");

await browser.close();

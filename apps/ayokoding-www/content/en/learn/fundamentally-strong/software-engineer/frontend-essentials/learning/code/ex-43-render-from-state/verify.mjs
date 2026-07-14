// ex-43: verify the rendered DOM matches the state object it was derived from (co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const h1 = await page.locator("#app h1").innerText();
const p = await page.locator("#app p").innerText();
console.log("rendered h1:", h1, "rendered p:", p);
if (h1 !== "Ada") throw new Error(`expected h1 "Ada", got "${h1}"`);
if (p !== "count: 3") throw new Error(`expected p "count: 3", got "${p}"`);
console.log("PASS: render(state) produced DOM that exactly matches the state object");

await browser.close();

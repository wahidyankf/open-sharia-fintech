// ex-44: verify mutating state then calling render() updates only the derived DOM text (co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const before = await page.locator("#count").innerText();
await page.evaluate(() => window.__bump());
const after = await page.locator("#count").innerText();
console.log("before:", before, "after mutate+render:", after);
if (before !== "count: 0") throw new Error(`unexpected initial render "${before}"`);
if (after !== "count: 1") throw new Error(`expected re-render to reflect new state, got "${after}"`);
console.log("PASS: mutating state and re-invoking render() produced DOM reflecting the new state");

await browser.close();

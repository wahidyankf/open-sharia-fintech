// ex-42: verify debouncing with setTimeout processes only the final value after rapid typing (co-17, co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const input = page.locator("#search");
// three rapid, value-replacing edits, each firing a fresh 'input' event that
// resets the 50ms debounce timer -- only the LAST one should ever fire the handler
await input.fill("a");
await input.fill("ab");
await input.fill("abc");
await page.waitForTimeout(150);
const processed = await page.locator("#processed").innerText();
const calls = await page.evaluate(() => window.__calls);
console.log("final processed value:", processed, "handler call count:", calls);
if (calls !== 1) throw new Error(`expected the debounced handler to run exactly once, ran ${calls} times`);
if (processed !== "abc") throw new Error(`expected the final value "abc", got "${processed}"`);

await browser.close();
console.log("PASS: debounce collapsed three rapid edits into exactly one processed call, on the final value");

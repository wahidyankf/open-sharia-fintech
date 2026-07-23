// ex-37: verify one listener on <ul> handles a click on any <li>, with the correct target (co-15, co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator('li[data-id="2"]').click();
const report = await page.locator("#report").innerText();
console.log("delegated report for clicking item 2:", report);
if (report !== "2") throw new Error(`expected "2", got "${report}"`);

await page.locator('li[data-id="3"]').click();
const report2 = await page.locator("#report").innerText();
console.log("delegated report for clicking item 3:", report2);
if (report2 !== "3") throw new Error(`expected "3", got "${report2}"`);
console.log("PASS: the single delegated listener resolved the correct target for two different items");

await browser.close();

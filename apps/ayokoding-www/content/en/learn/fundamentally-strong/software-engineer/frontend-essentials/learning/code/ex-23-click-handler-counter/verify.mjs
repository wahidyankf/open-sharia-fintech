// ex-23: verify the displayed count rises by one on each real click (co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const button = page.locator("#incr");
await button.click();
await button.click();
await button.click();
const text = await page.locator("#count").innerText();
console.log("count after three real clicks:", text);
if (text !== "3") {
  throw new Error(`expected "3" after three clicks, got "${text}"`);
}
console.log("PASS: three real clicks incremented the displayed count to 3");

await browser.close();

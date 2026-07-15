// ex-19: verify setting textContent updates the rendered text (co-13).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const text = await page.locator("#status").innerText();
console.log("#status rendered text:", text);
if (text !== "Ready") {
  throw new Error(`expected "Ready", got "${text}"`);
}
console.log("PASS: assigning textContent replaced the placeholder text on the rendered page");

await browser.close();

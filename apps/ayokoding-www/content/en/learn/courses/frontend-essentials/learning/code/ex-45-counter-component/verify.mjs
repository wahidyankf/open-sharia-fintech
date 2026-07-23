// ex-45: verify clicking the vanilla counter component increments the rendered number (co-20, co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#counter-btn").click();
await page.locator("#counter-btn").click();
const text = await page.locator("#counter-btn").innerText();
console.log("counter text after two clicks:", text);
if (text !== "Count: 2") throw new Error(`expected "Count: 2", got "${text}"`);
console.log("PASS: the counter component's state + re-render cycle incremented on each click");

await browser.close();

// ex-06: verify getComputedStyle(el).color reports the class rule's color (co-04).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const color = await page.locator(".btn").evaluate((el) => getComputedStyle(el).color);
console.log("computed color:", color);
if (color !== "rgb(220, 20, 20)") {
  throw new Error(`expected rgb(220, 20, 20), got ${color}`);
}
console.log("PASS: .btn class selector's color rule is the element's computed color");

await browser.close();

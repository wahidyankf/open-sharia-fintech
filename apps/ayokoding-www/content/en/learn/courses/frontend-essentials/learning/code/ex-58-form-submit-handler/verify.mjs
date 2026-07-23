// ex-58: verify the collected form data matches the real input values (co-22, co-16).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator('button[type="submit"]').click();
const collected = await page.locator("#collected").innerText();
console.log("collected data:", collected);
const parsed = JSON.parse(collected);
if (parsed.username !== "ada" || parsed.email !== "ada@example.com") {
  throw new Error(`collected data did not match inputs: ${collected}`);
}
console.log("PASS: the submit handler's collected data matched every real input value");

await browser.close();

// ex-26: verify two listeners on the same element both fire, in registration order (co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#btn").click();
const log = await page.evaluate(() => window.__log);
console.log("listener firing order:", JSON.stringify(log));
if (JSON.stringify(log) !== JSON.stringify(["first", "second"])) {
  throw new Error(`expected ["first","second"], got ${JSON.stringify(log)}`);
}
console.log("PASS: both click listeners fired, in the order they were registered");

await browser.close();

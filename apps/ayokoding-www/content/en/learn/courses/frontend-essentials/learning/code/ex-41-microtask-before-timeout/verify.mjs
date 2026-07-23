// ex-41: verify a Promise microtask runs before a setTimeout macrotask, even when the timeout is scheduled first (co-17).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.waitForFunction(() => window.__order.length === 2);
const order = await page.evaluate(() => window.__order);
console.log("execution order:", JSON.stringify(order));
if (JSON.stringify(order) !== JSON.stringify(["microtask", "timeout"])) {
  throw new Error(`unexpected order: ${JSON.stringify(order)}`);
}
console.log("PASS: the microtask ran before the timeout, despite being scheduled second");

await browser.close();

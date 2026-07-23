// ex-40: verify setTimeout(fn, 0) runs only after all the surrounding synchronous code (co-17).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.waitForFunction(() => window.__order.includes("timeout"));
const order = await page.evaluate(() => window.__order);
console.log("execution order:", JSON.stringify(order));
if (JSON.stringify(order) !== JSON.stringify(["sync-1", "sync-2", "timeout"])) {
  throw new Error(`unexpected order: ${JSON.stringify(order)}`);
}
console.log("PASS: both synchronous pushes ran before the setTimeout(fn, 0) callback");

await browser.close();

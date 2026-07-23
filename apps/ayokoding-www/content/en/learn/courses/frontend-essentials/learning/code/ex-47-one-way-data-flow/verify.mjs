// ex-47: verify the child reflects the parent's data and cannot write back up to it (co-19, co-18).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const childText = await page.locator("#child").innerText();
const parentLabelAfter = await page.evaluate(() => window.__parentLabel());
console.log("child rendered text:", childText, "parent's own state afterward:", parentLabelAfter);
if (childText !== "from parent") throw new Error(`expected child to reflect parent state, got "${childText}"`);
if (parentLabelAfter !== "from parent") {
  throw new Error("parent state must stay 'from parent' -- data flows one way only");
}

await browser.close();
console.log("PASS: child reflected the parent's data; the parent's own state was never mutated");

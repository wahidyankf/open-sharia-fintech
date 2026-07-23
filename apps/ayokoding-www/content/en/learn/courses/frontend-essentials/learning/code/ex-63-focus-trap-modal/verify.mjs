// ex-63: verify Tab cycles among the modal's own controls and never reaches the element outside it (co-26).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const seen = [await page.evaluate(() => document.activeElement.id)];
for (let i = 0; i < 4; i++) {
  await page.keyboard.press("Tab");
  seen.push(await page.evaluate(() => document.activeElement.id));
}
console.log("focus sequence over 4 Tabs:", JSON.stringify(seen));
if (seen.includes("outside")) {
  throw new Error("focus escaped the modal to the outside button");
}
if (JSON.stringify(seen) !== JSON.stringify(["first", "second", "last", "first", "second"])) {
  throw new Error(`unexpected trapped sequence: ${JSON.stringify(seen)}`);
}
console.log("PASS: Tab cycled first -> second -> last -> first, staying inside the modal every time");

await browser.close();

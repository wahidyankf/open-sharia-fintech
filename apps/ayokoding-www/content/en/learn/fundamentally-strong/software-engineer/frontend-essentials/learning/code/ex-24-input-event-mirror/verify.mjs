// ex-24: verify the span mirrors typed text live via the input event (co-14).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#name").fill("Ada Lovelace");
const mirrored = await page.locator("#mirror").innerText();
console.log("mirrored text:", mirrored);
if (mirrored !== "Ada Lovelace") {
  throw new Error(`expected "Ada Lovelace", got "${mirrored}"`);
}
console.log("PASS: the input event mirrored the typed text into the span live");

await browser.close();

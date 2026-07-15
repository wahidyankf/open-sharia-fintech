// ex-74: verify the derived total re-renders correctly whenever the underlying state changes (co-18, co-20).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const initial = await page.locator("#total").innerText();
console.log("initial total:", initial);
if (initial !== "Total: 20") throw new Error(`unexpected initial total: "${initial}"`);

await page.locator("#qty").fill("5");
const afterQty = await page.locator("#total").innerText();
console.log("total after changing qty to 5:", afterQty);
if (afterQty !== "Total: 50") throw new Error(`unexpected total: "${afterQty}"`);
console.log("PASS: the derived total recomputed correctly purely from the underlying state change");

await browser.close();

// ex-35: verify descendants recompute --brand once a .dark scope overrides it (co-06, co-11).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const lightColor = await page.locator("#light").evaluate((el) => getComputedStyle(el).color);
const darkColor = await page.locator("#dark").evaluate((el) => getComputedStyle(el).color);
console.log("light-scope color:", lightColor, "dark-scope color:", darkColor);
if (lightColor !== "rgb(10, 100, 200)") throw new Error("light scope did not use the root --brand");
if (darkColor !== "rgb(240, 200, 60)") throw new Error("dark scope did not recompute --brand");
console.log("PASS: the same .label rule resolved var(--brand) differently per cascade scope");

await browser.close();

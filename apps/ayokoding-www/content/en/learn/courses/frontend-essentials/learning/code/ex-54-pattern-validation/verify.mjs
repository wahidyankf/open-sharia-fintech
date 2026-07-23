// ex-54: verify a non-matching input fails validity against a pattern (co-23).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#code").fill("abcd");
const badValid = await page.locator("#code").evaluate((el) => el.checkValidity());
await page.locator("#code").fill("1234");
const goodValid = await page.locator("#code").evaluate((el) => el.checkValidity());
console.log("valid for 'abcd':", badValid, "valid for '1234':", goodValid);
if (badValid !== false) throw new Error("'abcd' should fail the [0-9]{4} pattern");
if (goodValid !== true) throw new Error("'1234' should satisfy the [0-9]{4} pattern");
console.log('PASS: pattern="[0-9]{4}" rejected non-matching input and accepted matching input');

await browser.close();

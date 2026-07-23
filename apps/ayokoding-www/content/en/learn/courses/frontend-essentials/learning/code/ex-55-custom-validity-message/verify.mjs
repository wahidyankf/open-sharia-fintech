// ex-55: verify setCustomValidity() surfaces the exact custom message on a mismatch (co-23).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

await page.locator("#confirm").fill("wrong");
const mismatchMessage = await page.locator("#confirm").evaluate((el) => el.validationMessage);
await page.locator("#confirm").fill("secret123");
const matchMessage = await page.locator("#confirm").evaluate((el) => el.validationMessage);
console.log("validationMessage on mismatch:", JSON.stringify(mismatchMessage));
console.log("validationMessage once matched:", JSON.stringify(matchMessage));
if (mismatchMessage !== "Passwords must match") {
  throw new Error(`expected the custom message, got "${mismatchMessage}"`);
}
if (matchMessage !== "") throw new Error("clearing custom validity should empty the message");
console.log("PASS: setCustomValidity('Passwords must match') was the exact reported message");

await browser.close();

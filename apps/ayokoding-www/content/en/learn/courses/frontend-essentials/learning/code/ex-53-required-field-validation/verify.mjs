// ex-53: verify checkValidity() reports invalid on an empty required field (co-23).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const emptyValid = await page.locator("#email").evaluate((el) => el.checkValidity());
await page.locator("#email").fill("person@example.com");
const filledValid = await page.locator("#email").evaluate((el) => el.checkValidity());
console.log("valid while empty:", emptyValid, "valid once filled:", filledValid);
if (emptyValid !== false) throw new Error("empty required field should report invalid");
if (filledValid !== true) throw new Error("a real, filled email should report valid");
console.log("PASS: checkValidity() correctly reported invalid-then-valid as the field was filled");

await browser.close();

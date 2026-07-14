// ex-08: verify the focused email input is styled and an unfocused input is not (co-04).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const emailBefore = await page.locator("#email").evaluate((el) => getComputedStyle(el).borderColor);
await page.locator("#email").focus();
const emailFocused = await page.locator("#email").evaluate((el) => getComputedStyle(el).borderColor);
const nameColor = await page.locator("#name").evaluate((el) => getComputedStyle(el).borderColor);
console.log("email border before focus:", emailBefore);
console.log("email border while focused:", emailFocused);
console.log("name (never focused) border:", nameColor);

if (emailFocused !== "rgb(0, 150, 80)") {
  throw new Error("focused email input did not receive the :focus rule");
}
if (nameColor === "rgb(0, 150, 80)") {
  throw new Error("unrelated text input should not match input[type=email]:focus");
}
console.log("PASS: input[type=email]:focus styles only the focused email input");

await browser.close();

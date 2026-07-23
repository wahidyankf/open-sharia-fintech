// ex-76: verify the real <button> is keyboard-operable and reports the button role natively (co-25, co-26).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const roleCount = await page.getByRole("button", { name: "Save" }).count();
console.log("elements exposing the button role named 'Save':", roleCount);
if (roleCount !== 1) throw new Error("expected a real button role, named 'Save'");

await page.locator("#save-btn").focus();
await page.keyboard.press("Enter");
const report = await page.locator("#report").innerText();
console.log("report after keyboard Enter:", report);
if (report !== "saved") throw new Error("a real <button> should activate on Enter with zero extra code");
console.log("PASS: the real <button> was keyboard-operable and exposed the button role with no extra ARIA");

await browser.close();

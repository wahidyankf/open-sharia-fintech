// ex-02: verify the accessibility tree exposes four landmark roles (co-02).
import { chromium } from "playwright";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("file://" + path.join(__dirname, "index.html"));

const banner = page.getByRole("banner");
const navigation = page.getByRole("navigation");
const main = page.getByRole("main");
const contentinfo = page.getByRole("contentinfo");

const counts = {
  banner: await banner.count(),
  navigation: await navigation.count(),
  main: await main.count(),
  contentinfo: await contentinfo.count(),
};
console.log("landmark counts:", JSON.stringify(counts));

for (const [role, count] of Object.entries(counts)) {
  if (count !== 1) {
    throw new Error(`expected exactly one ${role} landmark, found ${count}`);
  }
}
console.log("PASS: header/nav/main/footer expose banner/navigation/main/contentinfo roles");

await browser.close();

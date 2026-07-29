// Example 74: A Message Catalog with Interpolation. (co-35)
//
// A message catalog maps a message KEY to a locale-specific string with `{placeholder}` holes. A
// translate function interpolates values into the placeholders. Keeping strings in a catalog (not
// inline) is what lets translators work without touching component code.

// The catalog: locale -> key -> template string with {placeholders}.
type Catalog = Record<string, Record<string, string>>; // => nested locale -> key -> template

const messages: Catalog = {
  // => the same key, two locale-specific templates, each with a {name} hole
  en: { welcome: "Welcome, {name}!" }, // => English template
  id: { welcome: "Selamat datang, {name}!" }, // => Indonesian template
};

// translate resolves the key for the locale and interpolates {placeholders}.
function translate(locale: string, key: string, vars: Record<string, string>): string {
  // => co-35: resolve the template, then fill each {var} from the provided map
  const template = messages[locale]?.[key] ?? messages["en"][key]; // => fall back to English
  return template.replace(/\{(\w+)\}/g, (_, k: string) => vars[k] ?? `{${k}}`); // => fill holes
}

const en = translate("en", "welcome", { name: "Ada" }); // => English with the name filled in
const id = translate("id", "welcome", { name: "Ada" }); // => Indonesian with the name filled in

console.log(en); // => Output: Welcome, Ada!
console.log(id); // => Output: Selamat datang, Ada!

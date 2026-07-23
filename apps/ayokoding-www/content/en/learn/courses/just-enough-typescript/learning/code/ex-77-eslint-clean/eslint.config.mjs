// Example 77: eslint.config.mjs -- a minimal flat config (ESLint 9's default format).
import js from "@eslint/js"; // => the core "recommended" rule set, including no-unused-vars
import tsParser from "@typescript-eslint/parser"; // => lets ESLint's parser understand .ts syntax

export default [
  js.configs.recommended,
  {
    files: ["*.ts"],
    languageOptions: {
      parser: tsParser,
      parserOptions: { ecmaVersion: "latest", sourceType: "module" },
      globals: { console: "readonly" }, // => this example only needs the console global
    },
  },
];

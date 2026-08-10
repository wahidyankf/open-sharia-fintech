# beavernest-app-web

Vite CSR foundation-status client for BeaverNest. During local development it runs on loopback port
`19310` and proxies same-origin API requests to the loopback backend on `19320`. Production is the
combined `beavernest-be` ASP.NET image, which serves this static client on port `19300`.

## Quick Start

1. Create a developer-owned SQLite directory outside the repository.
2. Run `BEAVERNEST_BE_DEVELOPMENT_DATA_DIRECTORY=/absolute/path npm run beavernest:dev`.
3. Open <http://127.0.0.1:19310>.

## Commands

| Command                                      | Description                                    |
| -------------------------------------------- | ---------------------------------------------- |
| `nx dev beavernest-app-web`                  | Vite local development server                  |
| `nx build beavernest-app-web`                | Static `dist/` production build                |
| `nx run beavernest-app-web:test:quick`       | Unit, coverage, lint, and specification checks |
| `nx run beavernest-app-web:test:integration` | MSW client integration checks                  |

## Tech Stack

- Vite and React
- TypeScript and Tailwind v4
- Vitest and Playwright-BDD

The client has no runtime environment template: it uses same-origin API paths only.

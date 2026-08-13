# beavernest-app

Flutter Web client for the same-origin combined BeaverNest runtime. The production image builds
`build/web` and the F# backend serves it; this client does not own a development server, a runtime
environment file, or a service worker.

## Commands

```bash
npm exec nx run beavernest-app:build
npm exec nx run beavernest-app:test:quick
```

# Phase 2 unavailable diagnostics API evidence

`APP_ENV=test npm exec nx run beavernest-be-e2e:test:e2e` passed on 2026-08-13
(13 Playwright scenarios). Its disposable corrupted-SQLite fixture exercised
the hosted production image and asserted this complete sanitized 503 contract:

```http
HTTP/1.1 503 Service Unavailable
Cache-Control: no-store
Content-Type: application/json; charset=utf-8

{"status":"unavailable","components":{"database":"unavailable","schema":"unknown"}}
```

The bound assertion requires exactly the `status` and `components` top-level
keys, exactly `database` and `schema` component keys, and no cache validator.
It rejects `cause`, `version`, `uptimeSeconds`, `serverTimeUtc`, paths,
exceptions, SQL details, host identifiers, migration names, and every other
extra field.

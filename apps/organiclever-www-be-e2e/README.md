# organiclever-www-be-e2e

OrganicLever’s public site is a static marketing experience, so it has no separate backend API to
exercise. This project keeps the repository’s standard frontend/backend E2E shape intact while
making that absence explicit. 🧩

## What to run instead

Use the frontend suite when you want meaningful browser coverage:

```bash
npm exec nx -- run organiclever-www-fe-e2e:test:e2e
```

This project has a deliberately minimal placeholder scenario. Its commands are still useful for
checking the project wiring:

```bash
npm exec nx -- run organiclever-www-be-e2e:install
npm exec nx -- run organiclever-www-be-e2e:test:e2e
npm exec nx -- run organiclever-www-be-e2e:test:quick
```

The default target is `http://localhost:3200`; set `BASE_URL` only when checking another running
site. The placeholder behavior is documented in
[the OrganicLever public-site API slot](../../specs/apps/organiclever/www/behaviors/backend/README.md).

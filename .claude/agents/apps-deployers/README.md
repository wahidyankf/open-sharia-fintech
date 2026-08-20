---
title: "App Deployers"
description: "Deployer agents that push each app to its staging or production environment branch after validation."
---

# App Deployers

- [Apps Beavernest App Deployer](./apps-beavernest-app-deployer.md) — Triggers and monitors the scheduled beavernest-app-test-local-deploy-stag.yml GitHub Actions workflow, which validates the beavernest-app Flutter Web client (lint, widget, and browser E2E checks against a disposable combined-runtime container). No staging or production deploy target is provisioned yet — the workflow tests only and never pushes a stag branch. Deployment is deferred to a future plan.
- [Apps Beavernest Be Deployer](./apps-beavernest-be-deployer.md) — Triggers and monitors the scheduled beavernest-app-test-local-deploy-stag.yml GitHub Actions workflow, which validates the beavernest-be F#/Giraffe backend (integration tests against Dockerfile.integration, plus BE E2E against a disposable combined-runtime container). No staging or production deploy target is provisioned yet — the workflow tests only and never pushes a stag branch. Deployment is deferred to a future plan.
- [Apps Organiclever App Web Deployer](./apps-organiclever-app-web-deployer.md) — Deploys the OrganicLever app group to staging via the scheduled organiclever-app-test-local-deploy-stag.yml GitHub Actions workflow. The workflow runs the full local-stack test suite, then force-pushes the stag-organiclever-app-web and stag-organiclever-be branches. Vercel listens to stag-organiclever-app-web for automatic builds. Production promotion is deferred — no production-CD workflow exists yet.
- [Apps Organiclever Www Deployer](./apps-organiclever-www-deployer.md) — Deploys organiclever-www (OrganicLever marketing website) to production environment branch (prod-organiclever-www) after validation. Vercel listens to the production branch for automatic builds.
- [Apps Ose App Web Deployer](./apps-ose-app-web-deployer.md) — Deploys the OSE Application app group to staging via the scheduled ose-app-test-local-deploy-stag.yml GitHub Actions workflow. The workflow runs the full local-stack test suite, then force-pushes the stag-ose-app-web and stag-ose-be branches. Vercel listens to stag-ose-app-web for automatic builds. Production promotion is deferred — no production-CD workflow exists yet.
- [Apps Ose Www Deployer](./apps-ose-www-deployer.md) — Deploys ose-web to production environment branch (prod-ose-www) after validation. Vercel listens to production branch for automatic builds.
- [Apps Wahidyankf Www Deployer](./apps-wahidyankf-www-deployer.md) — Deploys wahidyankf-www to production environment branch (prod-wahidyankf-www) after validation. Vercel listens to production branch for automatic builds.
- [Apps Web Ui Storybook Deployer](./apps-web-ui-storybook-deployer.md) — Deploys web-ui Storybook to Vercel via force-push to prod-web-ui

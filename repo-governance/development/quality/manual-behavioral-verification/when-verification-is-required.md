---
title: "When Verification Is Required"
description: "The triggers that require manual behavioral verification."
category: explanation
subcategory: development
tags:
  - verification
  - testing
  - playwright
  - api
  - quality
  - manual-testing
created: 2026-04-04
when_to_use: "Use when deciding whether a change needs manual verification."
---

# When Verification Is Required

| Change Type                                 | UI Verification              | API Verification                       |
| ------------------------------------------- | ---------------------------- | -------------------------------------- |
| New UI page or component                    | Yes                          | No (unless it calls an API)            |
| UI bug fix                                  | Yes                          | No (unless the bug involved API calls) |
| New API endpoint                            | No (unless a UI consumes it) | Yes                                    |
| API behavior change                         | No (unless a UI consumes it) | Yes                                    |
| Full-stack feature (UI + API)               | Yes                          | Yes                                    |
| Styling-only change                         | Yes (visual check)           | No                                     |
| Internal refactor with no behavioral change | No                           | No                                     |
| Documentation-only change                   | No                           | No                                     |

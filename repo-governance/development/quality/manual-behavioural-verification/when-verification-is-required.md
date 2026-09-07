---
description: "The triggers that require manual behavioural verification."
when_to_use: "Use when deciding whether a change needs manual verification."
---

# When Verification Is Required

| Change Type                                  | UI Verification              | API Verification                       |
| -------------------------------------------- | ---------------------------- | -------------------------------------- |
| New UI page or component                     | Yes                          | No (unless it calls an API)            |
| UI bug fix                                   | Yes                          | No (unless the bug involved API calls) |
| New API endpoint                             | No (unless a UI consumes it) | Yes                                    |
| API behaviour change                         | No (unless a UI consumes it) | Yes                                    |
| Full-stack feature (UI + API)                | Yes                          | Yes                                    |
| Styling-only change                          | Yes (visual check)           | No                                     |
| Internal refactor with no behavioural change | No                           | No                                     |
| Documentation-only change                    | No                           | No                                     |

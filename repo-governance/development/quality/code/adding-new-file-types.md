---
description: "How to add a new file type to the pipeline."
when_to_use: "Use when a new file type needs lint coverage."
---

# Adding New File Types

To add Prettier formatting for new file types:

1. Update `lint-staged` configuration in `package.json`
2. Add new glob pattern and Prettier command
3. Test with a sample file
4. Commit the configuration change

**Example** (adding a new file type):

```json
{
  "lint-staged": {
    "*.toml": ["prettier --write"]
  }
}
```

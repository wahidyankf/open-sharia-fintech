---
description: "Language-specific code block indentation standards and purposeful use of bold, italic, inline code, and strikethrough"
when_to_use: "Read this when formatting a code block or deciding which inline text formatting to apply."
---

# Code Block and Text Formatting

## Code Block Formatting

**Code blocks follow language-specific indentation standards**.

**JavaScript/TypeScript** (2 spaces):

```javascript
function authenticate(user) {
  if (user.isValid) {
    return generateToken(user);
  }
  return null;
}
```

**Python** (4 spaces):

```python
def authenticate(user):
    if user.is_valid:
        return generate_token(user)
    return None
```

**YAML** (2 spaces):

```yaml
config:
  authentication:
    enabled: true
    provider: oauth2
```

**Guidelines**:

- **Always specify language** - Use syntax highlighting (e.g., ` ```javascript `)
- **Keep code examples minimal** - Show only relevant code
- **Include context** - Brief explanation before code block
- **Use realistic examples** - Actual patterns, not abstract foo/bar

## Text Formatting

**Use text formatting purposefully and consistently**.

### Bold Text

Use **bold** (`**text**`) for:

- **Key terms** on first mention
- **Important concepts** that need emphasis
- **UI element names** (buttons, menus)
- **Status labels** (Required, Optional)

PASS: **Good Use of Bold**:

```markdown
The **authentication token** expires after 1 hour. Click the **Login** button
to sign in.
```

FAIL: **Overuse of Bold**:

```markdown
The **authentication token** **expires** after **1 hour**. **Click** the
**Login button** to **sign in**.
```

### Italic Text

Use _italic_ (`*text*`) for:

- _Emphasis_ on specific words
- _Foreign terms_ or _Latin phrases_ (e.g., _et cetera_)
- _Variable names_ in prose (when not using code syntax)
- _Titles of books or publications_

PASS: **Good Use of Italic**:

```markdown
The _environment_ variable must be set _before_ running the application.
```

### Inline Code

Use inline code (`` `code` ``) for:

- `variable names`
- `function names`
- `file paths`
- `command names`
- `configuration keys`
- `HTTP status codes` (e.g., `200`, `404`)

PASS: **Good Use of Inline Code**:

```markdown
Set the `API_KEY` environment variable in your `.env` file. Run the
`npm install` command to install dependencies.
```

### Strikethrough

Use ~~strikethrough~~ (`~~text~~`) for:

- Deprecated features (with replacement noted)
- Corrections in changelog or updates

PASS: **Good Use of Strikethrough**:

```markdown
~~Use `legacy-auth`~~ **Deprecated** - Use `oauth2-auth` instead.
```

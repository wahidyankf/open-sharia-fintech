# Factual Validation — Common Validation Patterns

## Pattern 1: Command Syntax Validation

**Claim Type**: Bash/shell command syntax

**Validation Steps**:

1. Extract command and flags from content
2. WebSearch: "[command-name] official documentation"
3. WebFetch: Official CLI reference page
4. Compare: Flags, argument order, option names
5. Classify: [Verified] if exact match, [Error] if wrong

**Example**:

```
Content: "git commit -am 'message'"
WebSearch: "git commit flags official documentation"
WebFetch: https://git-scm.com/docs/git-commit
Verify: -a flag exists, -m flag exists, combined -am valid
Result: [Verified]
```

## Pattern 2: Version Number Validation

**Claim Type**: Software/package version reference

**Validation Steps**:

1. Extract package name and version number
2. WebSearch: "[package-name] [version] release"
3. WebFetch: Package registry page (npmjs.com, pypi.org)
4. Compare: Version exists in registry
5. Check: Latest version, deprecation status
6. Classify: [Verified], [Outdated], or [Error]

**Example**:

```
Content: "Install React 17.0.2"
WebSearch: "react 17.0.2 npmjs"
WebFetch: https://www.npmjs.com/package/react
Verify: 17.0.2 exists in version list
Check: Latest is 18.2.0 (major version ahead)
Result: [Outdated] - Breaking changes exist in v18
```

## Pattern 3: Code Example Validation

**Claim Type**: Code snippet correctness

**Validation Steps**:

1. Extract code example from content
2. Identify language and version
3. WebSearch: "[language] [concept] official examples"
4. WebFetch: Official documentation or tutorial
5. Compare: Syntax, method signatures, patterns
6. If possible: Run code locally to verify execution
7. Classify: [Verified], [Error], or [Outdated]

**Example**:

````markdown
Content:

```python
import asyncio
async def main():
    await asyncio.sleep(1)
asyncio.run(main())
```

WebSearch: "python asyncio.run documentation"
WebFetch: https://docs.python.org/3/library/asyncio-task.html
Verify: asyncio.run() syntax correct, requires Python 3.7+
Check: No syntax errors, runnable code
Result: [Verified]
````

## Pattern 4: API Method Validation

**Claim Type**: API method existence and signature

**Validation Steps**:

1. Extract API method name, parameters, return type
2. WebSearch: "[library] [method] official api documentation"
3. WebFetch: Official API reference
4. Compare: Method name, parameter types, return type
5. Check: Deprecation status
6. Classify: [Verified], [Error], or [Outdated]

**Example**:

```
Content: "Use fs.readFileSync(path, 'utf-8')"
WebSearch: "node.js fs.readFileSync official documentation"
WebFetch: https://nodejs.org/api/fs.html#fsreadfilesyncpath-options
Verify: Method exists, parameters match (path, options)
Check: 'utf-8' encoding valid
Result: [Verified]
```

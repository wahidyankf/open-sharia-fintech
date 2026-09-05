# Test Coverage Domain

Gherkin specs for rhino-cli test-coverage commands.

| File                             | Command                  | Scenarios |
| -------------------------------- | ------------------------ | --------- |
| `test-coverage-validate.feature` | `test-coverage validate` | 10        |

The corpus describes only commands exposed by the published Rhino process. Historical `diff` and
`merge` scenarios were retired because Rhino has no such public commands; internal coverage-map
helpers remain ordinary implementation details with focused Unit regressions.

## Related

- **Parent**: [gherkin](../README.md)

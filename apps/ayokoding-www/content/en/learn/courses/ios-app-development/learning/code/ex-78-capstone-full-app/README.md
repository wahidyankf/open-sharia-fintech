# Example 78 source

Example 78 is the complete, runnable Focus List app rather than a duplicate snippet. Its exact app,
unit-test, and UI-test sources are colocated at `../../capstone/code/FocusList.swift`,
`../../capstone/code/FocusListTests.swift`, and `../../capstone/code/FocusListUITests.swift`.

Add those files to a SwiftUI `FocusList` app target plus its XCTest and UI-test targets, then run:

```bash
xcodebuild test -scheme FocusList -destination 'platform=iOS Simulator,name=iPhone 16'
```

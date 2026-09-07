---
description: "Specifies the first three required parts of a cookbook recipe: the recipe title format, problem statement, and solution code."
when_to_use: "Read when drafting the title, problem statement, and solution code of a cookbook recipe."
---

# Recipe Structure Standards: Title, Problem Statement, and Solution

Each cookbook recipe MUST follow this structure:

## 1. Recipe Title

**Format**: `## Recipe: [Problem Statement]`

**Examples**:

- `## Recipe: Read CSV File with Headers`
- `## Recipe: Retry Failed API Calls with Exponential Backoff`
- `## Recipe: Parse JSON with Unknown Schema`

**Requirements**:

- Clear problem statement (what this solves)
- Action-oriented (verb + object)
- Specific enough to be searchable
- No difficulty indicators (not "Beginner: Read CSV")

## 2. Problem Statement

**Format**: 1-3 sentences describing the specific problem.

**Example**:

```markdown
### Problem

You need to read a CSV file with headers into a list of objects, handling missing values and type conversions automatically. The CSV may have inconsistent formatting (extra spaces, quoted fields).
```

**Requirements**:

- State the problem clearly and specifically
- Include constraints or edge cases
- Mention common pain points
- Keep focused (one problem per recipe)

## 3. Solution

**Format**: Annotated code with `// =>` or `# =>` notation showing the complete solution.

**Example**:

```go
package main

import (
    "encoding/csv"     // => Standard library CSV parser
    "os"               // => For file operations
    "strings"          // => For trimming whitespace
)

func readCSV(filepath string) ([]map[string]string, error) {
    file, err := os.Open(filepath)  // => Open file for reading
    if err != nil {
        return nil, err             // => Return error if file doesn't exist
    }
    defer file.Close()              // => Ensure file is closed when done

    reader := csv.NewReader(file)   // => Create CSV reader
    reader.TrimLeadingSpace = true  // => Remove extra spaces automatically

    headers, err := reader.Read()   // => Read first row as headers
    if err != nil {
        return nil, err
    }

    var records []map[string]string // => Store results as key-value maps
    for {
        row, err := reader.Read()   // => Read each subsequent row
        if err == io.EOF {          // => End of file reached
            break
        }
        if err != nil {
            return nil, err         // => Handle malformed CSV
        }

        record := make(map[string]string)
        for i, value := range row {
            if i < len(headers) {   // => Prevent index out of bounds
                record[headers[i]] = value
            }
        }
        records = append(records, record)
    }

    return records, nil
}
```

**Requirements**:

- Complete, runnable code (not pseudocode)
- Copy-paste ready with all imports
- Annotations using `// =>` or `# =>` notation
- Annotation density: 0.5-1.5 lines per code line (lighter than by-example's 1-2.25)
- Focus annotations on "what this does" not "why we need this"

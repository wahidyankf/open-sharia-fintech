# Developing AI Agents — Selecting AI Models: Decision Framework

## Available Models

### Sonnet (claude-sonnet-4-5)

**Characteristics**:

- Advanced reasoning capabilities
- Complex decision-making
- Deep pattern recognition
- Sophisticated analysis
- Multi-step orchestration
- Higher cost, slower performance

**Use for**: Complex, reasoning-intensive tasks

### Haiku (claude-haiku-3-5)

**Characteristics**:

- Fast execution
- Straightforward tasks
- Pattern matching
- Simple decision-making
- Cost-effective
- Lower cost, faster performance

**Use for**: Simple, well-defined tasks

## Decision Framework

### Use Sonnet When Task Requires

✅ **Advanced Reasoning**

- Analyzing technical claims for subtle contradictions
- Distinguishing objective errors from subjective improvements
- Detecting false positives in validation findings
- Context-dependent decision-making
- Inferring user intent from ambiguous requests

✅ **Complex Pattern Recognition**

- Cross-referencing multiple documentation files
- Identifying conceptual duplications (not just verbatim)
- Detecting inconsistencies across architectural layers
- Understanding domain-specific patterns
- Recognizing semantic similarities

✅ **Sophisticated Analysis**

- Verifying factual accuracy against authoritative sources
- Assessing confidence levels (HIGH/MEDIUM/FALSE_POSITIVE)
- Evaluating code quality and architectural decisions
- Analyzing narrative flow and pedagogical structure
- Determining fix safety and impact

✅ **Multi-Step Orchestration**

- Coordinating complex validation workflows
- Managing dependencies between validation steps
- Iterative refinement processes
- Dynamic workflow adaptation
- Error recovery and retry logic

✅ **Deep Web Research**

- Finding and evaluating authoritative sources
- Comparing claims against official documentation
- Version verification across multiple registries
- API correctness validation
- Detecting outdated information

### Use Haiku When Task Is

✅ **Pattern Matching**

- Extracting URLs from markdown files
- Finding code blocks by language
- Matching file naming patterns
- Regular expression searches
- Simple syntax validation

✅ **Sequential Execution**

- File existence checks
- URL accessibility validation
- Cache file reading/writing
- Date comparisons
- Status reporting

✅ **Straightforward Validation**

- Checking if files exist
- Verifying link format (contains `.md`)
- Counting lines or characters
- Comparing timestamps
- Simple YAML/JSON parsing

✅ **No Complex Reasoning**

- Tasks with clear pass/fail criteria
- No ambiguity or judgment required
- Deterministic outcomes
- No context analysis needed
- No trade-off decisions

✅ **High-Volume Processing**

- Checking hundreds of links
- Validating many files
- Batch operations
- Performance-critical tasks
- Cost-sensitive operations

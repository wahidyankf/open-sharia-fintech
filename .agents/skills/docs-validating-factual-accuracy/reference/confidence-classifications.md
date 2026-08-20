# Factual Validation — The Four Confidence Classifications

All validation findings use one of four confidence labels:

**[Verified]** - Objectively correct according to authoritative sources

- Command syntax matches official documentation
- Version number confirmed via package registry
- Code example compiles/runs as shown
- API method exists with correct signature

**[Error]** - Objectively incorrect, breaks functionality

- Command syntax wrong (fails when executed)
- Code example won't compile/run
- API method doesn't exist or has wrong signature
- Incorrect version number that doesn't exist

**[Outdated]** - Was correct but now superseded by newer version

- References old major version with breaking changes
- Uses deprecated API (still works but replacement exists)
- Command syntax changed in recent release
- Configuration format updated

**[Unverified]** - Cannot confirm correctness (insufficient evidence)

- No authoritative source found
- Multiple conflicting sources
- Documentation ambiguous or incomplete
- Claim too specific to verify externally

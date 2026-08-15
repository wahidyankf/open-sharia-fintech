# Synthetic local finding report

## LAB-001 — broken access-control model

- **Reproduction**: Review the supplied synthetic owner-mismatch record; do not send a request.
- **Impact**: In the fictional training application, a peer record could be disclosed.
- **Severity rationale**: High in this deliberately vulnerable local model because confidentiality is affected.
- **Remediation**: Enforce server-side subject, action, and object authorization; add a peer-access regression test.

## LAB-002 — injection-boundary model

- **Reproduction**: Review the supplied synthetic query-construction marker; do not submit input.
- **Impact**: In the fictional training application, untrusted data could be interpreted as query text.
- **Severity rationale**: High in this deliberately vulnerable local model because data integrity may be affected.
- **Remediation**: Use parameter binding, remove string-built queries, and add a regression test with adversarial fixture input.

## Cleanup record

Only bundled synthetic local evidence was read. No network traffic was sent, no credentials were used,
and no target outside the authorized local scope was touched.

---
title: "Mitigate, Validate, Detect"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

1. Inventory endpoints, data classifications, trust boundaries, and OWASP-relevant abuse cases.
2. Implement authenticated authorization checks, input validation, safe error handling, security headers,
   least privilege, and secret references from the local environment.
3. Validate the hardened service with harmless, lab-local negative tests that previously reproduced a
   documented weakness.
4. Turn each attempted abuse into a low-noise detection mapped to ATT&CK where appropriate.
5. Write `posture.md`: weakness → mitigation → failed validation attempt → detection evidence.

```python
def authorize(subject: str | None, owner: str) -> bool:
    return subject is not None and subject == owner
```

Authentication is not authorization: the test matrix must prove both identity and object-level access
control. Use real OAuth2/OIDC integration only in a reader-controlled environment.

## Remote-backend decision artifact

This runnable example intentionally uses Terraform's `local` backend so `terraform init` never
contacts a cloud endpoint. It demonstrates the backend configuration boundary without pretending a
learning artifact is a team-safe shared backend.

Before a team selects a remote backend, record these decisions:

- Which approved service stores encrypted state and state backups?
- Which service provides state locking, and how is a stale lock investigated?
- Which workload identities may read state, and which may write it?
- How are secret-bearing state snapshots retained, audited, and restored?

Do not copy an S3 backend block from this course into a real environment. Select a provider-approved,
lock-capable backend through your organization's security and platform review.

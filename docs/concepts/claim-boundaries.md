# Claim Boundaries

A claim boundary is the line between what a lane proved and what remains
unverified.

Good agent receipts make both sides visible:

- Claim proven: local tests pass for the contract checker.
- Claim not proven: no host checkout, runtime export, live config, or external
  service was checked.

This phrasing is not bureaucracy. It prevents source-only work from being
mistaken for deployment proof.

## Common boundaries

| Boundary | Use when |
| --- | --- |
| `repo_only` | The change was checked locally in source. |
| `github_coordination` | Issue, PR, branch, or CI state was checked. |
| `host_checkout_only` | A target host checkout was verified. |
| `runtime_export_only` | A runtime export or running service was checked. |
| `live_config_only` | Redacted live config shape or freshness was checked. |
| `external_service_only` | A bounded external service probe was checked. |
| `end_to_end` | Source continuity and downstream live proof were both checked. |
| `handoff` | Source is ready, but another surface must still be checked. |
| `blocked` | Work stopped for a concrete reason. |

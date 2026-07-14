# GitHub Actions examples

These workflows show three common `repo_only` lanes using the commands shipped
in Homelab Operator `v1.0.0`:

| Workflow | Check | Expected result |
| --- | --- | --- |
| [`receipt-check.yml`](workflows/receipt-check.yml) | Validate a checked-in lane receipt on pull requests that change receipts. | `RECEIPT_CONTRACT_OK` |
| [`privacy-scan.yml`](workflows/privacy-scan.yml) | Scan repository text on pull requests and pushes to `main`. | `PRIVACY_SCAN_OK` |
| [`scheduled-source-check.yml`](workflows/scheduled-source-check.yml) | Validate a source claim and scan repository text on a weekly or manual run. | `SURFACE_CLAIM_OK`, then `PRIVACY_SCAN_OK` |

Copy the workflow you need into `.github/workflows/`. Change every synthetic
file path to the matching receipt or claim in your repository, including any
`paths` filter, then keep the proof-boundary comments with the copied workflow.

All three workflows use read-only GitHub permissions and disable persisted Git
credentials. They prove only that the checked-out files passed the listed
source checks. They do not prove host checkout, runtime export, live config,
deployment, or external service health.

There is no generic JSON Schema workflow yet. Add one only after the planned
schema-validation CLI command is available.

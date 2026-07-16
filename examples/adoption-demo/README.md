# Adoption Demo

This is a short, fully synthetic demo that shows a new adopter how to run
a source-only check from a clean checkout. No private infrastructure, live
services, runtime state, or real hostnames are used.

## What This Demo Proves

A `repo_only` check proves that local source, documentation, schema, and
contract checks are coherent. It does not prove host checkout, runtime
export, live config, external service status, or end-to-end operation.

## Quick Start

Install the development package from the repository root:

```bash
python -m pip install -e ".[dev]"
```

Run the source-only demo flow:

```bash
homelab-operator check-pr --body-file examples/demo/corrected-pr-body.md
homelab-operator check-receipt --file examples/demo/merge-ready-receipt.md
homelab-operator check-estate --file examples/minimal-homelab/estate.yaml
homelab-operator doctor --root .
homelab-operator check-privacy --root .
```

## Expected Output

```text
PR_CONTRACT_OK
RECEIPT_CONTRACT_OK
ESTATE_CONTRACT_OK
PR_CONTRACT_OK
RECEIPT_CONTRACT_OK
SURFACE_CLAIM_OK
ESTATE_CONTRACT_OK
PRIVACY_SCAN_OK
HOMELAB_OPERATOR_DOCTOR_OK
PRIVACY_SCAN_OK
```

All output comes from synthetic fixtures. Nothing above is runtime or
live-service proof.

## Understanding the Output

| Output line | What it proves | What it does not prove |
| --- | --- | --- |
| `PR_CONTRACT_OK` | PR body states a valid claim boundary | Host checkout, runtime, live config |
| `RECEIPT_CONTRACT_OK` | Lane receipt is structurally valid | Any surface beyond source |
| `ESTATE_CONTRACT_OK` | Estate YAML schema is valid | Real infrastructure matches |
| `PRIVACY_SCAN_OK` | No private material found in text files | Runtime secrets or env |
| `HOMELAB_OPERATOR_DOCTOR_OK` | All repo contract fixtures pass | Anything beyond the repo |

## Claim Boundary

Proof kind: repo_only

Claim proven: the commands above pass against synthetic fixtures in a local
checkout.

Claim not proven: no host checkout, runtime export, live config, deployment,
package publish, or external service was checked.

Host/runtime/live-config handoff needed: no

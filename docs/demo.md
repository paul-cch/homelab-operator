# Demo

This demo is a synthetic terminal walk-through for a source-only documentation
change. It shows an unsafe pull request body failing, a corrected pull request
body passing, a merge-ready receipt template, and a green project doctor run.

All paths and outputs are public examples. They do not include private
hostnames, addresses, logs, runtime state, live config, secrets, or external
service proof.

## Replay Commands

Run from the repository root after installing the development package:

```bash
set +e
homelab-operator check-pr --body-file examples/demo/unsafe-pr-body.md
unsafe_status=$?
set -e
printf 'unsafe_status=%s\n' "$unsafe_status"

homelab-operator check-pr --body-file examples/demo/corrected-pr-body.md
homelab-operator receipt-template --state MERGE_READY
homelab-operator check-receipt --file examples/demo/merge-ready-receipt.md
homelab-operator doctor --root .
```

## Expected Transcript

```text
$ homelab-operator check-pr --body-file examples/demo/unsafe-pr-body.md
ERROR PR body must state the source/host/runtime/live-config claim boundary

$ unsafe_status=$?
$ printf 'unsafe_status=%s\n' "$unsafe_status"
unsafe_status=1

$ homelab-operator check-pr --body-file examples/demo/corrected-pr-body.md
PR_CONTRACT_OK

$ homelab-operator receipt-template --state MERGE_READY
## Agent Lane Receipt

- Exit state: MERGE_READY
- Issue:
- Branch / worktree:
- PR:
- Owned paths:
- Surface classification:
- Proof kind:
- Claim proven:
- Claim not proven:
- Repo gate:
- Host/runtime handoff needed:
- Host gate needed:
- Runtime gate needed:
- Live config gate needed:
- Checks or commands run:
- Blockers:
- Next safe command:

$ homelab-operator check-receipt --file examples/demo/merge-ready-receipt.md
RECEIPT_CONTRACT_OK

$ homelab-operator doctor --root .
PR_CONTRACT_OK
RECEIPT_CONTRACT_OK
SURFACE_CLAIM_OK
ESTATE_CONTRACT_OK
PRIVACY_SCAN_OK
HOMELAB_OPERATOR_DOCTOR_OK
```

## Claim Boundary

The corrected example uses `repo_only` proof. It proves only that the local
source and documentation checks are coherent. It does not prove host checkout,
runtime export, live config, external service status, or end-to-end operation.

## Summary

Update synthetic dashboard documentation without claiming runtime status.

## Linked Issue

Refs #204

## Owned Paths

- `docs/demo.md`
- `examples/demo/corrected-pr-body.md`

## Validation

- `python -m pytest` passed for local source checks.
- `homelab-operator doctor --root .` passed.

## Claim Boundary

Proof kind: repo_only.

Claim proven: local source, documentation, and contract checks are coherent.

Claim not proven: no host checkout, runtime export, live config, external service, or end-to-end operation was checked.

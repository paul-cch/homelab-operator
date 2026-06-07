# Add a pre-commit hook for local contract checks

Labels: `good first issue`, `roadmap`, `developer-experience`

## Summary

Provide a documented `pre-commit` hook configuration for running Homelab
Operator checks before contributors commit contract files.

## Why

Many adopters catch formatting and lint issues before CI. A pre-commit example
would let maintainers catch unsafe PR bodies, receipts, claims, estate files,
and privacy leaks earlier in the workflow.

## Proposed Scope

- Add a `.pre-commit-hooks.yaml` entry or documented local hook example.
- Support running `homelab-operator check-privacy --root .`.
- Include examples for contract fixtures or common generated paths.
- Document installation and usage in a short synthetic example.

## Acceptance Criteria

- The hook can run locally after installing the package.
- Tests or a smoke check cover the hook command target.
- Documentation states which files are scanned.
- The example avoids private paths and real operational identifiers.

## Out Of Scope

- Enforcing the hook on all contributors.
- Replacing CI checks.
- Installing hooks automatically during package installation.

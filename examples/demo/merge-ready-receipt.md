## Agent Lane Receipt

- Exit state: MERGE_READY
- Issue: Refs #204
- Branch / worktree: codex/demo-asset-synthetic
- PR: not opened in this demo
- Owned paths: docs/demo.md, examples/demo/*
- Surface classification: repo source
- Proof kind: repo_only
- Claim proven: synthetic demo files and local contract checks are coherent
- Claim not proven: no host checkout, runtime export, live config, external service, or end-to-end operation was checked
- Repo gate: `python -m pytest` and `homelab-operator doctor --root .` passed
- Host/runtime handoff needed: no
- Host gate needed: no
- Runtime gate needed: no
- Live config gate needed: no
- Checks or commands run: `homelab-operator check-pr --body-file examples/demo/corrected-pr-body.md`; `homelab-operator check-receipt --file examples/demo/merge-ready-receipt.md`; `homelab-operator doctor --root .`
- Blockers: none
- Next safe command: open pull request

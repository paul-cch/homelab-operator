## Agent Lane Receipt

- Exit state: MERGE_READY
- Issue: Refs #1
- Branch / worktree: example/source-change
- PR: example only
- Owned paths: examples/minimal-homelab/estate.yaml
- Surface classification: repo source
- Proof kind: repo_only
- Claim proven: example estate shape was reviewed in source
- Claim not proven: no fake host, runtime, live config, or external service was checked
- Repo gate: `homelab-operator check-receipt --file examples/minimal-homelab/receipts/source-change.md`
- Host/runtime handoff needed: no
- Host gate needed: no
- Runtime gate needed: no
- Live config gate needed: no
- Checks or commands run: receipt contract check
- Blockers: none
- Next safe command: open pull request

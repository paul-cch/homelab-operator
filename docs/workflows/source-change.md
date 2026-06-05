# Source Change Workflow

Use this workflow when an agent changes repo-managed files but does not mutate
host, runtime, live config, or external services.

1. Read the nearest repo instructions.
2. Create a branch or worktree.
3. Record owned paths before editing.
4. Make the smallest reviewable source change.
5. Run the relevant repo gate.
6. Open a pull request with a clear claim boundary.
7. End with a lane receipt.

The valid proof kind for this workflow is usually `repo_only`. If the source
change requires a later deploy or live check, end with `HOST_RUNTIME_HANDOFF`
instead of claiming end-to-end success.

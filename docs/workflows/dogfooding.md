# Dogfooding Homelab Operator

Use this workflow when Homelab Operator is applied to its own pull requests.
The point is not to prove a private homelab is healthy. The point is to show
that the public repository can police its own PR bodies, lane receipts, examples,
schemas, and privacy boundaries.

## Rule

Treat this repository like any other adopter:

1. Name the owned paths before editing.
2. Run the repo gate that matches the change.
3. Validate the PR body with `homelab-operator check-pr`.
4. End the work with a lane receipt.
5. Keep the proof kind at `repo_only` unless a public example proves a wider
   surface.

Dogfooding must stay public and synthetic. Do not add private hostnames,
addresses, domains, logs, runtime state, live config, secrets, or personal
operating history to examples.

## Public Example: PR #1

[PR #1](https://github.com/paul-cch/homelab-operator/pull/1) is a useful public
example because it used the project vocabulary on the project itself.

The PR body stated:

- summary of the source changes
- linked issue status of `None supplied.`
- owned paths for schemas, contracts, tests, privacy coverage, and a repo map
- validation commands for install, tests, lint, doctor, contract checks, privacy
  scan, build, and package checks
- claim boundary with `Proof kind: repo_only`

For PR #1, `repo_only` proved that the local repository checkout had coherent
source, schemas, tests, docs artifact, package build, and privacy scan results.
It did not prove that any host had pulled the branch, that any runtime export
was current, that live config was checked, that an external service was healthy,
or that a release/deployment surface was exercised.

That boundary is the dogfood story: Homelab Operator can make its own public PR
reviewable without pretending a source-only check is operational proof.

## Synthetic Receipt

The receipt in
[`examples/dogfood/pr-1-repo-only-receipt.md`](../../examples/dogfood/pr-1-repo-only-receipt.md)
is synthetic. It is modeled on the public PR #1 body, but it is not a claim that
private infrastructure was inspected.

Use the example to check receipt shape:

```bash
homelab-operator check-receipt --file examples/dogfood/pr-1-repo-only-receipt.md
```

Expected result:

```text
RECEIPT_CONTRACT_OK
```

## What To Copy

Copy the discipline, not private evidence:

- keep owned paths explicit
- run the smallest relevant repo gate
- record what `repo_only` proved
- record what it did not prove
- use `HOST_RUNTIME_HANDOFF` when a later host or runtime check is needed
- leave private runtime and live-config details out of public examples

# Proof Ladder

Homelab Operator separates claims by surface. A maintainer should be able to
read a pull request or receipt and know exactly what was proven.

## Repo source

Repo proof means local code, docs, schemas, templates, or tests were checked. It
does not prove that a host pulled the change or that a runtime is using it.

## GitHub coordination

GitHub proof means issues, pull requests, branches, CI state, and review
metadata are current. It does not prove live infrastructure state by itself.

## Host checkout

Host checkout proof means the target host has the intended source and host-side
checks passed. It does not prove runtime export state unless export checks ran.

## Runtime export

Runtime export proof means the target runtime was checked directly. Without
source continuity, it does not prove a particular branch or commit is deployed.

## Live config

Live config proof means redacted configuration structure, ownership, or
freshness was checked. It must not print secret values and it does not prove
source deployment.

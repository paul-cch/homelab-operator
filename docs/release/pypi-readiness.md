# PyPI Readiness

This checklist prepares a future maintainer to publish `homelab-operator`
through PyPI Trusted Publishing. It is a readiness gate only: do not publish,
create tags, create releases, dispatch workflows, change secrets, or change
GitHub/PyPI settings from a documentation or source-polish branch.

## Trusted Publishing Shape

Use tokenless publishing through the existing GitHub Actions workflow:

- PyPI project: `homelab-operator`
- GitHub repository: `paul-cch/homelab-operator`
- Workflow file: `.github/workflows/publish.yml`
- PyPI Trusted Publisher workflow name: `publish.yml`
- GitHub environment: `pypi`
- Publish action: `pypa/gh-action-pypi-publish@release/v1`

The PyPI Trusted Publisher configuration must match the repository, workflow
filename, and environment exactly. The GitHub `pypi` environment should require
maintainer approval before the publish job can exchange its OIDC token for a
short-lived PyPI upload token. Do not add PyPI API tokens or passwords as
repository secrets.

## Version, Tag, And Release

Keep these surfaces distinct:

- Package version: the `project.version` value in `pyproject.toml`; this is
  the version PyPI accepts and it cannot be reused after publication.
- Git tag: a `vX.Y.Z` pointer to the exact commit being published.
- GitHub release: the human-facing release record attached to the tag.

Do not publish when these disagree. A release branch or PR may update the
package version and changelog before a tag exists, but the eventual workflow
dispatch should run from the reviewed tag or exact commit intended for PyPI.

## Readiness Checklist

1. Scope and privacy
   - Working tree contains only intended release changes.
   - Public docs, examples, package metadata, screenshots, and release notes
     contain no private hostnames, IP addresses, domains, logs, runtime state,
     live config, secrets, personal data, or assistant memory payloads.
   - Any package description or README text is based on public examples only.

2. Version and release state
   - `pyproject.toml` has the intended PEP 440 package version.
   - `CHANGELOG.md` has the matching release entry or reviewed Unreleased
     entry that will become the release entry.
   - The intended PyPI version has not already been published.
   - The intended tag and GitHub release plan match the package version.

3. Package checks
   - Install development dependencies and run the source validation ladder:

     ```bash
     python -m pip install -e ".[dev]"
     python -m pytest
     homelab-operator doctor --root .
     homelab-operator check-privacy --root .
     ```

   - Build fresh artifacts and check package metadata:

     ```bash
     rm -rf dist
     python -m build
     python -m twine check dist/*
     ```

   - Inspect artifact contents before publishing:

     ```bash
     python -m tarfile -l dist/*.tar.gz
     python -m zipfile -l dist/*.whl
     ```

   - Confirm `dist/` contains only the intended source distribution and wheel.

4. Trusted Publishing approval
   - PyPI has a Trusted Publisher entry for the repository, `publish.yml`, and
     the `pypi` environment.
   - GitHub has a protected `pypi` environment with required maintainer
     approval.
   - The workflow dispatch version input equals `project.version`.
   - The workflow dispatch confirmation phrase is entered deliberately.
   - The environment approval is reviewed by a maintainer who checked this
     readiness list.

## Explicit Non-goals

- Do not publish to PyPI from this checklist.
- Do not create tags, GitHub releases, or release branches from this checklist.
- Do not dispatch `.github/workflows/publish.yml` from this checklist.
- Do not add PyPI API tokens, passwords, secrets, or secret-like settings.
- Do not change GitHub environment protection or PyPI project settings here.
- Do not claim host, runtime, live config, deployment, or external-service
  proof from package checks.

## Stop Conditions

Pause before publishing if package checks fail, the worktree is dirty with
unreviewed changes, the version/tag/release surfaces disagree, the PyPI Trusted
Publisher identity is uncertain, the `pypi` environment lacks maintainer
approval, or any private operational detail appears in a file that would be
published or shown publicly.

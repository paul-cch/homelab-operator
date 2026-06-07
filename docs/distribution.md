# Distribution

Homelab Operator is packaged as a Python CLI. Distribution work must stay
public and privacy-safe: do not include private hostnames, IP addresses,
domains, logs, runtime state, live config, or secrets in package metadata,
release notes, examples, screenshots, or PyPI project text.

## Install From Source

Use a source checkout when testing unreleased changes:

```bash
python -m pip install -e ".[dev]"
homelab-operator doctor --root .
```

For an isolated CLI install from a checkout:

```bash
pipx install .
homelab-operator --help
```

To reinstall after local changes:

```bash
pipx reinstall homelab-operator
```

## Install From PyPI

After a maintainer publishes the package to PyPI, users should prefer `pipx`
for the command-line app:

```bash
pipx install homelab-operator
homelab-operator doctor --root .
```

Project-local installs can use pip:

```bash
python -m pip install homelab-operator
```

## Status And Badges

Current distribution status: source installs are supported; PyPI publication is
a manual future release step.

Useful badge snippets for public docs:

```markdown
[![CI](https://github.com/paul-cch/homelab-operator/actions/workflows/ci.yml/badge.svg)](https://github.com/paul-cch/homelab-operator/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/homelab-operator.svg)](https://pypi.org/project/homelab-operator/)
[![Python](https://img.shields.io/pypi/pyversions/homelab-operator.svg)](https://pypi.org/project/homelab-operator/)
[![License](https://img.shields.io/pypi/l/homelab-operator.svg)](https://github.com/paul-cch/homelab-operator/blob/main/LICENSE)
```

Add the PyPI badges only after the PyPI project exists.

## Release Checklist

1. Confirm the working tree contains only intended public-safe source and docs
   changes.
2. Update `version` in `pyproject.toml`.
3. Add a matching entry to `CHANGELOG.md`.
4. Run the source validation ladder:

   ```bash
   python -m pip install -e ".[dev]"
   python -m pytest
   homelab-operator doctor --root .
   ```

5. Build and inspect package artifacts:

   ```bash
   rm -rf dist
   python -m build
   python -m twine check dist/*
   ```

6. Confirm `dist/` contains only the intended sdist and wheel for the release.
7. Create the tag or GitHub release only after review.
8. Publish to PyPI as a separate manual action.

Before any real publish, complete the compact PyPI readiness gate in
[`docs/release/pypi-readiness.md`](release/pypi-readiness.md).

## Manual PyPI Publish

Publishing is intentionally manual. Do not publish from ordinary documentation
or source-polish branches.

Recommended future setup:

1. Create the `homelab-operator` project on PyPI.
2. Configure PyPI Trusted Publishing for this GitHub repository and the
   `Publish to PyPI` workflow.
3. Protect the GitHub `pypi` environment with maintainer approval.
4. Run the workflow manually from the reviewed tag or release branch.
5. Enter the exact version from `pyproject.toml` and the confirmation phrase
   requested by the workflow.

The workflow should build fresh artifacts, run `twine check`, and then publish
through PyPI Trusted Publishing. Do not store PyPI API tokens in the repository.

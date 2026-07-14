from __future__ import annotations

import re
from pathlib import Path

from homelab_operator.cli import main


ROOT = Path(__file__).parents[1]
WORKFLOWS = ROOT / "examples/github-actions/workflows"
EXPECTED_ACTION_REFS = {
    "actions/checkout": "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
    "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",
    "actions/upload-artifact": "043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
    "actions/download-artifact": "3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c",
    "pypa/gh-action-pypi-publish": "release/v1",
}
ACTION_REF_PATTERN = re.compile(r"uses:\s+([^@\s]+)@([^\s#]+)")
ACTION_SOURCES = (
    *sorted((ROOT / ".github/workflows").glob("*.yml")),
    *sorted((ROOT / "templates/github/workflows").glob("*.yml")),
    *sorted(WORKFLOWS.glob("*.yml")),
    ROOT / "src/homelab_operator/scaffold.py",
)
EXAMPLES = {
    "receipt-check.yml": "homelab-operator check-receipt --file examples/minimal-homelab/receipts/source-change.md",
    "privacy-scan.yml": "homelab-operator check-privacy --root .",
    "scheduled-source-check.yml": (
        "homelab-operator check-claim --json-file examples/github-actions/repo-source-claim.json"
    ),
}


def test_github_action_examples_are_read_only_repo_only_workflows() -> None:
    for filename in EXAMPLES:
        workflow = (WORKFLOWS / filename).read_text(encoding="utf-8")

        assert "Proof kind: repo_only" in workflow
        assert "Claim proven:" in workflow
        assert "Claim not proven:" in workflow
        assert "host checkout, runtime export, live config, or external service" in workflow
        assert "permissions:\n  contents: read" in workflow
        assert "persist-credentials: false" in workflow
        assert "HOMELAB_OPERATOR_REF: v1.0.0" in workflow
        assert f"actions/checkout@{EXPECTED_ACTION_REFS['actions/checkout']}" in workflow
        assert f"actions/setup-python@{EXPECTED_ACTION_REFS['actions/setup-python']}" in workflow
        assert "validate-schema" not in workflow


def test_repository_action_refs_use_reviewed_refs() -> None:
    found_actions: set[str] = set()

    for path in ACTION_SOURCES:
        source = path.read_text(encoding="utf-8")
        for action, ref in ACTION_REF_PATTERN.findall(source):
            found_actions.add(action)
            assert action in EXPECTED_ACTION_REFS, (
                f"{path.relative_to(ROOT)} has unreviewed action {action}@{ref}"
            )
            assert ref == EXPECTED_ACTION_REFS[action], (
                f"{path.relative_to(ROOT)} has stale {action}@{ref}"
            )

    assert found_actions == set(EXPECTED_ACTION_REFS)


def test_github_action_examples_use_the_documented_released_commands() -> None:
    for filename, command in EXAMPLES.items():
        workflow = (WORKFLOWS / filename).read_text(encoding="utf-8")
        assert command in workflow

    receipt = (WORKFLOWS / "receipt-check.yml").read_text(encoding="utf-8")
    assert "pull_request:" in receipt
    assert '"examples/minimal-homelab/receipts/**"' in receipt

    privacy = (WORKFLOWS / "privacy-scan.yml").read_text(encoding="utf-8")
    assert "pull_request:" in privacy
    assert "push:" in privacy

    scheduled = (WORKFLOWS / "scheduled-source-check.yml").read_text(encoding="utf-8")
    assert "schedule:" in scheduled
    assert "workflow_dispatch:" in scheduled


def test_github_action_example_inputs_pass_the_cli() -> None:
    assert main(
        [
            "check-receipt",
            "--file",
            "examples/minimal-homelab/receipts/source-change.md",
        ]
    ) == 0
    assert main(
        [
            "check-claim",
            "--json-file",
            "examples/github-actions/repo-source-claim.json",
        ]
    ) == 0
    assert main(["check-privacy", "--root", "."]) == 0

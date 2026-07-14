from __future__ import annotations

from pathlib import Path

from homelab_operator.cli import main


ROOT = Path(__file__).parents[1]
WORKFLOWS = ROOT / "examples/github-actions/workflows"
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
        assert "actions/checkout@v4" in workflow
        assert "actions/setup-python@v5" in workflow
        assert "validate-schema" not in workflow


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

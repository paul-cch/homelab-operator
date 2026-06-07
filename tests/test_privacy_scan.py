from __future__ import annotations

import pytest

from homelab_operator.contracts import scan_privacy


def dotted(*octets: int) -> str:
    return ".".join(str(octet) for octet in octets)


@pytest.mark.parametrize(
    "address",
    [
        dotted(10, 0, 0, 42),
        dotted(127, 0, 0, 1),
        dotted(172, 16, 0, 8),
        dotted(172, 31, 255, 9),
        dotted(192, 168, 12, 34),
    ],
)
def test_privacy_scan_rejects_loopback_and_private_addresses(address: str) -> None:
    result = scan_privacy(f"synthetic endpoint address: {address}")

    assert not result.ok
    assert any("192\\.168" in error or "172\\." in error or "127" in error or "10" in error for error in result.errors)


@pytest.mark.parametrize(
    "address",
    [
        dotted(172, 15, 0, 8),
        dotted(172, 32, 0, 8),
        dotted(192, 0, 2, 10),
        dotted(198, 51, 100, 22),
        dotted(203, 0, 113, 44),
    ],
)
def test_privacy_scan_accepts_adjacent_and_documentation_addresses(address: str) -> None:
    result = scan_privacy(f"public documentation example address: {address}")

    assert result.ok


@pytest.mark.parametrize(
    ("name", "separator"),
    [
        ("api_key", " = "),
        ("access-token", ": "),
        ("password", "='"),
        ("authorization", ': "'),
    ],
)
def test_privacy_scan_rejects_credential_assignments(name: str, separator: str) -> None:
    assignment = f"{name}{separator}synthetic-placeholder"

    result = scan_privacy(assignment)

    assert not result.ok
    assert any(
        "authorization" in error
        or "api[_-]?key" in error
        or "access[_-]?token" in error
        or "password" in error
        for error in result.errors
    )


@pytest.mark.parametrize(
    "key_prefix",
    [
        "",
        "RSA ",
        "OPENSSH ",
    ],
)
def test_privacy_scan_rejects_private_key_blocks(key_prefix: str) -> None:
    key_block = (
        f"-----BEGIN {key_prefix}PRIVATE KEY-----\n"
        "synthetic-placeholder\n"
        f"-----END {key_prefix}PRIVATE KEY-----"
    )

    result = scan_privacy(key_block)

    assert not result.ok
    assert any("PRIVATE KEY" in error for error in result.errors)


def test_privacy_scan_accepts_safe_public_policy_text() -> None:
    text = f"""Public contribution policy:
- Use synthetic fixtures and documentation examples such as {dotted(203, 0, 113, 7)}.
- Mention that secrets, credentials, private topology, and raw logs must stay out of the repo.
- Keep proof labels source-only unless a public example validates a wider claim.
"""

    result = scan_privacy(text)

    assert result.ok

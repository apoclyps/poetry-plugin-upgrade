import pytest
from poetry.core.packages.package import Package

from tests.helpers import TestUpgradeCommand


@pytest.mark.parametrize(
    ("current_version", "available_version", "expected_version", "_name"),
    [
        # Happy path tests
        ("0.0.1", "1.0.0", "1.0.0", "happy_path_no_operator"),
        ("^0.0.1", "1.0.0", "^1.0.0", "happy_path_caret"),
        ("~0.0.1", "1.0.0", "~1.0.0", "happy_path_tilde_zero"),
        (">=0.0.1", "1.0.0", ">=1.0.0", "happy_path_greater_equal"),
        ("==0.0.1", "1.0.0", "==1.0.0", "happy_path_equal"),
        (">0.0.1", "1.0.0", ">1.0.0", "happy_path_greater"),
        # Edge cases
        ("<0.0.1", "1.0.0", "<0.0.1", "happy_path_less_equal"),
        ("<=0.0.1", "1.0.0", "<=0.0.1", "happy_path_less_equal"),
    ],
)
def test_handle_version(
    current_version: str,
    available_version: str,
    expected_version: str,
    _name: str,
    upgrade_cmd_tester: TestUpgradeCommand,
):
    candidate = Package(
        name="test_package",
        version=available_version,
    )

    version = upgrade_cmd_tester.handle_version(current_version=current_version, candidate=candidate)

    assert version == expected_version

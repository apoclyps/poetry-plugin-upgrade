from unittest.mock import Mock

from poetry.core.packages.dependency import Dependency
from poetry.core.packages.package import Package
from pytest_mock import MockerFixture
from tomlkit import parse

from tests.helpers import TestUpgradeCommand


def test_handle_dependency(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="^1.0",
        groups=["main"],
    )
    new_version: str = "2.0.0"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=False,
        pinned=False,
        only_packages=[],
        exclude=[],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=False,
    )

    selector.find_best_candidate.assert_called_once_with(
        package_name=dependency.name,
        target_package_version=dependency.pretty_constraint,
        allow_prereleases=dependency.allows_prereleases(),
        source=dependency.source_name,
    )
    bump_version_in_pyproject_content.assert_called_once_with(
        dependency=dependency,
        new_version=f"^{new_version}",
        pyproject_content=content,
    )


def test_handle_dependency_with_pinned_version(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="1.0",
        groups=["main"],
    )
    new_version: str = "2.0.0"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=False,
        pinned=True,
        only_packages=[],
        exclude=[],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=False,
    )

    selector.find_best_candidate.assert_called_once_with(
        package_name=dependency.name,
        target_package_version=dependency.pretty_constraint,
        allow_prereleases=dependency.allows_prereleases(),
        source=dependency.source_name,
    )
    bump_version_in_pyproject_content.assert_called_once_with(
        dependency=dependency,
        new_version=new_version,
        pyproject_content=content,
    )


def test_handle_dependency_with_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="^1.0",
        groups=["main"],
    )
    new_version: str = "2.0.0"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=True,
        pinned=True,
        only_packages=[],
        exclude=[],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=False,
    )

    selector.find_best_candidate.assert_called_once_with(
        package_name=dependency.name,
        target_package_version="*",
        allow_prereleases=dependency.allows_prereleases(),
        source=dependency.source_name,
    )
    bump_version_in_pyproject_content.assert_called_once_with(
        dependency=dependency,
        new_version=f"^{new_version}",
        pyproject_content=content,
    )


def test_handle_dependency_with_zero_caret(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="^0",
        groups=["main"],
    )
    new_version: str = "0.1"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=True,
        pinned=False,
        only_packages=[],
        exclude=[],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=False,
    )

    selector.find_best_candidate.assert_called_once_with(
        package_name=dependency.name,
        target_package_version="*",
        allow_prereleases=dependency.allows_prereleases(),
        source=dependency.source_name,
    )
    bump_version_in_pyproject_content.assert_called_once_with(
        dependency=dependency,
        new_version=f"^{new_version}",
        pyproject_content=content,
    )


def test_handle_dependency_excluded(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="^1.0",
        groups=["main"],
    )
    new_version: str = "2.0.0"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=False,
        pinned=False,
        only_packages=[],
        exclude=["foo"],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=False,
    )

    selector.find_best_candidate.assert_not_called()
    bump_version_in_pyproject_content.assert_not_called()


def test_handle_dependency_preserve_wildcard(
    upgrade_cmd_tester: TestUpgradeCommand,
    mocker: MockerFixture,
) -> None:
    dependency: Dependency = Dependency(
        name="foo",
        constraint="*",
        groups=["main"],
    )
    new_version: str = "2.0.0"
    package: Package = Package(
        name=dependency.name,
        version=new_version,
    )

    content = parse("")

    selector = Mock()
    selector.find_best_candidate = Mock(return_value=package)
    bump_version_in_pyproject_content = mocker.patch(
        "poetry_plugin_upgrade.command.UpgradeCommand.bump_version_in_pyproject_content",
        return_value=None,
    )

    upgrade_cmd_tester.handle_dependency(
        dependency=dependency,
        latest=True,
        pinned=False,
        only_packages=[],
        exclude=[],
        pyproject_content=content,
        selector=selector,
        preserve_wildcard=True,
    )

    selector.find_best_candidate.assert_not_called()
    bump_version_in_pyproject_content.assert_not_called()

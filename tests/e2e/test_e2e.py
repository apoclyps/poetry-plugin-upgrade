from pathlib import Path

from cleo.testers.application_tester import ApplicationTester
from poetry.core.packages.package import Package
from poetry.pyproject.toml import PyProjectTOML
from pytest_mock import MockerFixture


def test_command(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("upgrade") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_latest(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    path = project_path / "expected_pyproject_with_latest.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("upgrade --latest") == 0
    assert dict(PyProjectTOML(tmp_pyproject_path).file.read()) == expected
    command_call.assert_called_once_with(name="update")


def test_command_with_dry_run(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path).file.read()

    assert app_tester.execute("upgrade --dry-run") == 0
    # assert pyproject.toml file not modified
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_not_called()


def test_command_with_no_install(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    path = project_path / "expected_pyproject.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("upgrade --no-install") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="lock", args="--no-update")


def test_command_reverts_pyproject_on_error(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        side_effect=Exception,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    expected = PyProjectTOML(tmp_pyproject_path).file.read()

    assert app_tester.execute("upgrade") == 1
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_pinned_without_latest_fails(app_tester: ApplicationTester) -> None:
    assert app_tester.execute("upgrade --pinned") == 1


def test_command_with_exclude(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    path = project_path / "expected_pyproject_with_exclude.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("upgrade --exclude foo --exclude bar --exclude=grault") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_command_preserve_wildcard(
    app_tester: ApplicationTester,
    packages: list[Package],
    mocker: MockerFixture,
    project_path: Path,
    tmp_pyproject_path: Path,
) -> None:
    command_call = mocker.patch(
        "poetry.console.commands.command.Command.call",
        return_value=0,
    )
    mocker.patch(
        "poetry.version.version_selector.VersionSelector.find_best_candidate",
        side_effect=packages,
    )
    mocker.patch(
        "poetry.console.commands.installer_command.InstallerCommand.reset_poetry",
        return_value=None,
    )

    path = project_path / "expected_pyproject_with_latest_and_preserve_wildcard.toml"
    expected = PyProjectTOML(path).file.read()

    assert app_tester.execute("upgrade --latest --preserve-wildcard") == 0
    assert PyProjectTOML(tmp_pyproject_path).file.read() == expected
    command_call.assert_called_once_with(name="update")


def test_preserve_wildcard_without_latest_fails(
    app_tester: ApplicationTester,
) -> None:
    assert app_tester.execute("upgrade --preserve-wildcard") == 1

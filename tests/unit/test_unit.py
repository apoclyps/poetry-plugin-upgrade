from poetry.core.packages.dependency import Dependency
from tomlkit import parse

from src.poetry_plugin_upgrade.command import is_pinned
from tests.helpers import TestUpgradeCommand


def test_bump_version_in_pyproject_content(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependencies = [
        Dependency(
            name="foo",
            constraint="^1.0",
            groups=["main"],
        ),
        Dependency(
            name="bar",
            constraint="^1.0",
            groups=["main"],
            optional=True,
        ),
        Dependency(
            name="baz",
            constraint="^1.0",
            groups=["dev"],
        ),
    ]

    content = parse(
        """
        [tool.poetry.dependencies]
        python = "^3.7"
        foo = "^1.0"
        bar = { version = "^1.1", optional = true }

        [tool.poetry.group.dev.dependencies]
        baz = "^1.2"
        """
    )

    for dependency in dependencies:
        new_version = "^1.9"
        upgrade_cmd_tester.bump_version_in_pyproject_content(
            dependency=dependency,
            new_version=new_version,
            pyproject_content=content,
        )

    poetry_content = content["tool"]["poetry"]
    assert poetry_content["dependencies"]["foo"] == new_version
    assert poetry_content["dependencies"]["bar"]["version"] == new_version
    assert poetry_content["group"]["dev"]["dependencies"]["baz"] == new_version


def test_bump_version_in_pyproject_content_with_old_dev_dependencies(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependencies = [
        Dependency(
            name="foo",
            constraint="^1.0",
            groups=["main"],
        ),
        Dependency(
            name="bar",
            constraint="^1.0",
            groups=["main"],
            optional=True,
        ),
        Dependency(
            name="baz",
            constraint="^1.0",
            groups=["dev"],
        ),
    ]

    content = parse(
        """
        [tool.poetry.dependencies]
        python = "^3.7"
        foo = "^1.0"
        bar = { version = "^1.1", optional = true }

        [tool.poetry.dev-dependencies]
        baz = "^1.2"
        """
    )

    for dependency in dependencies:
        new_version = "^1.9"
        upgrade_cmd_tester.bump_version_in_pyproject_content(
            dependency=dependency,
            new_version=new_version,
            pyproject_content=content,
        )

    poetry_content = content["tool"]["poetry"]
    assert poetry_content["dependencies"]["foo"] == new_version
    assert poetry_content["dependencies"]["bar"]["version"] == new_version
    assert poetry_content["dev-dependencies"]["baz"] == new_version


def test_is_bumpable_is_false_when_source_type_is_git(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
        source_type="git",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_source_type_is_file(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
        source_type="file",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_source_type_is_directory(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
        source_type="directory",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_name_is_python(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(name="python", constraint="^1.2.3")
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_dependency_not_in_only_packages(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(name="foo", constraint="^1.2.3")
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=["bar"],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_pinned(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_wildcard(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_less_than(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="<1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_greater_than(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint=">1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_less_than_or_equal(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="<=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_inequality(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="!=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_version_multiple_requirements(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint=">=1.2.3, <2.0.0",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_true_when_version_caret(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="^1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_tilde(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="~1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_greater_than_or_equal(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint=">=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_tilde_pep440(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="~=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=False,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_false_when_version_pinned_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_true_when_version_pinned_and_latest_and_pinned(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=True,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_pinned() -> None:
    assert is_pinned("1.1.1")
    assert is_pinned("==1.1.1")
    assert not is_pinned("^1.1.1")
    assert not is_pinned(">=1.1.1")
    assert not is_pinned("~1.1.1")


def test_is_bumpable_is_false_when_version_pinned_with_with_equals_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="==1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_true_when_version_wildcard_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_less_than_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="<1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_greater_than_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint=">1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_true_when_version_less_than_or_equal_and_latest(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="<=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=[],
        preserve_wildcard=False,
    )
    assert is_bumpable is True


def test_is_bumpable_is_false_when_dependency_excluded(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="<=1.2.3",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=["foo"],
        preserve_wildcard=False,
    )
    assert is_bumpable is False


def test_is_bumpable_is_false_when_preserve_wildcard(
    upgrade_cmd_tester: TestUpgradeCommand,
) -> None:
    dependency = Dependency(
        name="foo",
        constraint="*",
    )
    is_bumpable = upgrade_cmd_tester.is_bumpable(
        dependency=dependency,
        only_packages=[],
        latest=True,
        pinned=False,
        exclude=["foo"],
        preserve_wildcard=False,
    )
    assert is_bumpable is False

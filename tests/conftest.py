from pathlib import Path

import pytest
from cleo.testers.application_tester import ApplicationTester
from poetry.core.packages.dependency_group import DependencyGroup
from poetry.core.packages.package import Package
from poetry.factory import Factory
from poetry.poetry import Poetry
from poetry.pyproject.toml import PyProjectTOML
from tomlkit.toml_document import TOMLDocument

from tests.helpers import TestApplication, TestUpgradeCommand


@pytest.fixture()
def project_path() -> Path:
    return Path(__file__).parent / "fixtures" / "simple_project"


@pytest.fixture()
def pyproject_content(project_path: Path) -> TOMLDocument:
    path = project_path / "pyproject.toml"

    return PyProjectTOML(path).file.read()


@pytest.fixture()
def expected_pyproject_content(project_path: Path) -> TOMLDocument:
    path = project_path / "expected_pyproject.toml"

    return PyProjectTOML(path).file.read()


@pytest.fixture()
def tmp_pyproject_path(
    tmp_path_factory: pytest.TempPathFactory,
    pyproject_content: TOMLDocument,
) -> Path:
    tmp_pyproject_path = tmp_path_factory.mktemp("simple_project") / "pyproject.toml"
    tmp_pyproject_path.write_text(pyproject_content.as_string())

    return tmp_pyproject_path


@pytest.fixture()
def app_tester(tmp_pyproject_path: Path) -> ApplicationTester:
    poetry = Factory().create_poetry(tmp_pyproject_path)
    app = TestApplication(poetry)

    return ApplicationTester(app)


@pytest.fixture()
def poetry(project_path: Path) -> Poetry:
    return Factory().create_poetry(project_path)


@pytest.fixture()
def upgrade_cmd_tester(poetry: Poetry) -> TestUpgradeCommand:
    return TestUpgradeCommand(poetry)


@pytest.fixture()
def groups(poetry: Poetry) -> list[DependencyGroup]:
    return poetry.package._dependency_groups.values()  # noqa: SLF001


@pytest.fixture()
def packages() -> list[Package]:
    return [
        Package(name="foo", version="2.2.2"),
        Package(name="bar", version="2.2.2"),
        Package(name="baz", version="2.2.2"),
        Package(name="corge", version="2.2.2"),
        Package(name="grault", version="2.2.2"),
        Package(name="garply", version="2.2.2"),
        Package(name="waldo", version="2.2.2"),
        Package(name="fred", version="2.2.2"),
        Package(name="plugh", version="2.2.2"),
        Package(name="xyzzy", version="2.2.2"),
        Package(name="nacho", version="2.2.2"),
        Package(name="thud", version="2.2.2"),
        Package(name="foobar", version="2.2.2"),
        Package(name="foobaz", version="2.2.2"),
        Package(name="fooqux", version="2.2.2"),
        Package(name="fooquux", version="2.2.2"),
        Package(name="foo-corge", version="2.2.2"),
    ]

from typing import Any

from poetry.console.application import Application
from poetry.poetry import Poetry
from poetry_plugin_upgrade.command import UpgradeCommand


class TestUpgradeCommand(UpgradeCommand):
    def __init__(self, poetry: Poetry) -> None:
        super().__init__()
        self._poetry = poetry

    __test__ = False

    def line(self, data: Any):
        print(data)


class TestApplication(Application):
    def __init__(self, poetry: Poetry) -> None:
        super().__init__()
        self._poetry = poetry

from typing import Self

from poetry.plugins.application_plugin import ApplicationPlugin

import poetry_plugin_upgrade
from poetry_plugin_upgrade.command import UpgradeCommand


def factory() -> UpgradeCommand:
    return UpgradeCommand()


class UpgradeApplicationPlugin(ApplicationPlugin):
    def activate(self: Self, application: poetry_plugin_upgrade) -> None:
        application.command_loader.register_factory("upgrade", factory)

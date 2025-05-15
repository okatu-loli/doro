from ..system_tray import SystemTray
from ..config import Config
from ..ResourceManager import ResourceManager
from ..pet_window import PetWindow


class MainLayer:
    """全局管理层"""

    def __init__(self) -> None:
        self.config: Config = Config(self)
        self.resource_manager: ResourceManager = ResourceManager(
            Config.PATH_CONFIG["Resources"], self
        )
        self.pet_window: PetWindow = PetWindow(self.config, self)
        self.system_tray: SystemTray = SystemTray(self.pet_window, self.config, self)


__all__ = [
    "MainLayer",
]

import os

from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon, QAction
from PySide6.QtWidgets import (
    QSystemTrayIcon,
    QMenu,
)


from .config import Config
from .pet_window import PetWindow
from .setting_gui import SettingsDialog

if TYPE_CHECKING:
    from MainLayer import MainLayer


class SystemTray:

    def __init__(
        self, pet_window: PetWindow, config: Config, main_layer: "MainLayer"
    ) -> None:
        self.pet_window: PetWindow = pet_window
        self.config: Config = config
        self.main_layer: MainLayer = main_layer

        # 创建系统托盘图标
        self.tray_icon: QSystemTrayIcon = QSystemTrayIcon()

        # 加载图标
        icon_path: str = Config.PATH_CONFIG["Icon"]["RelativePath"]
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            print(f"警告: 图标文件不存在: {icon_path}")

        # 创建托盘菜单
        self.menu = QMenu()

        # 添加菜单项
        self.show_action = QAction("显示桌宠", self.menu)
        self.show_action.triggered.connect(self.show_pet)
        self.menu.addAction(self.show_action)

        self.hide_action = QAction("隐藏桌宠", self.menu)
        self.hide_action.triggered.connect(self.hide_pet)
        self.menu.addAction(self.hide_action)

        self.menu.addSeparator()

        self.settings_action = QAction("设置", self.menu)
        self.settings_action.triggered.connect(self.show_settings)
        self.menu.addAction(self.settings_action)

        self.menu.addSeparator()

        self.quit_action = QAction("关闭程序", self.menu)
        self.quit_action.triggered.connect(self.quit_application)
        self.menu.addAction(self.quit_action)

        # 设置托盘菜单
        self.tray_icon.setContextMenu(self.menu)

    def show_tray_icon(self):
        """显示托盘图标"""
        self.tray_icon.show()

    def hide_tray_icon(self):
        """隐藏托盘图标"""
        self.tray_icon.hide()

    def show_pet(self):
        """显示桌宠"""
        self.pet_window.show()

    def hide_pet(self):
        """隐藏桌宠"""
        self.pet_window.hide()

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self.config, self.pet_window)
        dialog.exec()

    def quit_application(self):
        """退出应用程序"""
        self.tray_icon.hide()
        self.pet_window.close()
        os._exit(0)

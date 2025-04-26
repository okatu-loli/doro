import os
import sys

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from src.pet_window import PetWindow
from src.system_tray import SystemTray
from src.config import Config


def main():
    # 初始化配置
    config: Config = Config()

    # 创建Qt应用PySide6>=6.5.0
    app = QApplication(sys.argv)

    # 创建主窗口
    pet_window: PetWindow = PetWindow(config)

    # 创建系统托盘
    system_tray = SystemTray(pet_window, config)

    # 显示主窗口
    system_tray.show_tray_icon()
    system_tray.show_pet()

    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

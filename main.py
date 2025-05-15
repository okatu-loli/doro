import os
import sys

from typing import NoReturn

from src.MainLayer import MainLayer
from src.state.base_state import PetState

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication


def main() -> NoReturn:
    app = QApplication(sys.argv)

    try:
        global_layer = MainLayer()
    except Exception as e:
        print(f"Error initializing MainLayer: {e}")
        sys.exit(1)

    global_layer.system_tray.show_tray_icon()
    global_layer.system_tray.show_pet()
    global_layer.pet_window.state_machine.transition_to(PetState.NORMAL)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

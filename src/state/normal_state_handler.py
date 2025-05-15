import os
import random
from PySide6.QtCore import QEvent, Qt, QTimer
from PySide6.QtGui import QMouseEvent, QIcon
from PySide6.QtWidgets import QMessageBox
from ..setting_gui import SettingsDialog
from .base_state import StateHandler, menu_item, PetState
from ..style_sheet import (
    generate_messagebox_css,
)
from ..setting_gui import SettingsDialog


@menu_item("关于Doro", "handle_about", isGlobal=0)
@menu_item("设置", "handle_settings", separator=True, isGlobal=1)
class NormalStateHandler(StateHandler):
    """正常状态处理器"""

    def _init_state(self):
        self.normal_timer = QTimer()
        self.normal_timer.timeout.connect(self.change_gif)
        return super()._init_state()

    def on_enter(self):
        self.normal_timer.start(
            1000 * self.main_layer.config.config["Random"]["Interval"]
        )
        gif_path = random.choice(self.main_layer.resource_manager.get_gif("Common"))
        self.main_layer.pet_window.play_gif(gif_path)

    def on_exit(self):
        self.normal_timer.stop()
        return super().on_exit()

    def handle_event(self, event: QEvent) -> bool:
        if isinstance(event, QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonPress:
                return self._handle_mouse_press(event)
            elif event.type() == QEvent.Type.MouseButtonDblClick:
                return self._handle_double_click(event)
        return False

    def update_config(self):
        self.normal_timer.stop()
        self.normal_timer.start(
            1000 * self.main_layer.config.config["Random"]["Interval"]
        )
        return super().update_config()

    def _handle_mouse_press(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.state_machine.transition_to(PetState.DRAGGING)
            return True
        return False

    def _handle_double_click(self, event: QMouseEvent) -> bool:
        """处理鼠标双击事件"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.state_machine.transition_to(PetState.CLICKED)
            return True
        return False

    def change_gif(self):
        if self.state_machine.current_state == PetState.NORMAL:
            gif_path = random.choice(self.main_layer.resource_manager.get_gif("Common"))
            self.main_layer.pet_window.play_gif(gif_path)

    def handle_about(self):
        """处理关于"""
        self.show_about_info()

    def handle_settings(self):
        """处理设置"""
        self.show_settings()

    def show_settings(self):
        """显示设置对话框"""
        dialog = SettingsDialog(self.main_layer.config, self.main_layer.pet_window)
        dialog.exec()

    def show_about_info(self):
        """显示关于信息"""
        about_text = """Doro 桌宠使用指南
        
人，你来啦


1. 基本交互
   - 拖动: 按住左键拖动动画区域。
   - 双击: 双击动画区域播放特殊动画。
   - 右键菜单: 点击动画区域弹出菜单。
     - 喂食哦润吉 🍊: 恢复饥饿值。
     - 关于Doro: 显示此指南。

2. 主要功能
   - 动画: 多种状态动画。
   - 随机移动: 不时在屏幕上走动。
   - 系统信息: 显示 CPU、内存、网速。
   - 主题: 可在设置中更改。

3. 系统托盘图标
   - 右键点击托盘图标可进行显示/隐藏、设置、关闭等操作。
        """
        msg_box = QMessageBox(self.main_layer.pet_window)
        msg_box.setWindowTitle("关于 Doro 宠物")
        msg_box.setText(about_text)
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "favicon.ico"
        )
        if os.path.exists(icon_path):
            msg_box.setWindowIcon(QIcon(icon_path))
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.setStyleSheet(generate_messagebox_css())
        msg_box.exec()

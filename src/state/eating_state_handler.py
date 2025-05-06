from PySide6.QtCore import QTimer, QEvent, Qt
from PySide6.QtGui import QMouseEvent
from .base_state import StateHandler, PetState


class EatingStateHandler(StateHandler):
    """进食状态处理器"""

    def _init_state(self):
        return super()._init_state()

    def on_enter(self):
        self.pet_window.play_gif(self.pet_window.eat_gif_path)
        QTimer.singleShot(3000, self._on_eating_end)  # type: ignore[call-arg-type]

    def on_exit(self):
        return super().on_exit()

    def handle_event(self, event: QEvent) -> bool:
        if isinstance(event, QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonPress:
                return self._handle_mouse_press(event)
        return False

    def update_config(self):
        return super().update_config()

    def _handle_mouse_press(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.state_machine.transition_to(PetState.DRAGGING)
            return True
        return False

    def _on_eating_end(self):
        """进食结束"""
        self.state_machine.pop_state()

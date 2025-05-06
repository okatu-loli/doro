import random
from PySide6.QtCore import QTimer, QEvent, Qt
from PySide6.QtGui import QMouseEvent
from .base_state import StateHandler, PetState


class MovingStateHandler(StateHandler):
    """移动状态处理器"""

    def _init_state(self):
        # 随机移动定时器
        self.random_move_timer = QTimer()
        self.random_move_timer.timeout.connect(self.start_random_movement)
        # 根据配置决定是否启动随机移动
        if self.pet_window.config.config["Workspace"]["AllowRandomMovement"]:
            print(
                "启动随机移动",
                self.pet_window.config.config["Random"]["Interval"] * 1000,
            )
            self.random_move_timer.start(
                self.pet_window.config.config["Random"]["Interval"] * 1000
            )
        return super()._init_state()

    def on_enter(self):
        print("进来了")
        if not self.check_can_random_move():
            return False
        self.prepare_movement()

    def on_exit(self):
        self.pet_window.move_timer.stop()
        self.pet_window.is_moving = False
        return

    def handle_event(self, event: QEvent) -> bool:
        if (
            isinstance(event, QMouseEvent)
            and event.type() == QEvent.Type.MouseButtonPress
        ):
            if event.button() == Qt.MouseButton.LeftButton:
                self.state_machine.transition_to(PetState.DRAGGING)
                return True
        return False

    def update_config(self):
        return super().update_config()

    def check_can_random_move(self):
        """检查是否可以随机移动"""
        return (
            self.state_machine.current_state in [PetState.NORMAL]
            and self.pet_window.config.config["Workspace"]["AllowRandomMovement"]
        )

    def start_random_movement(self):
        """启动随机移动"""
        if (
            not self.pet_window.is_moving
            and random.random() < 0.1
            and self.check_can_random_move()
        ):
            self.state_machine.transition_to(PetState.MOVING)

    def prepare_movement(self):
        """准备移动动画和方向，自动适配 GIF 方向"""
        self.pet_window.move_direction = random.choice(["left", "right", "up", "down"])
        move_gif = random.choice(self.pet_window.move_gif_paths)

        # 右移时镜像
        mirror = self.pet_window.move_direction == "right"
        self.pet_window.play_gif(move_gif, mirror=mirror)

        self.pet_window.move_duration = random.randint(5000, 10000)
        self.pet_window.is_moving = True
        self.pet_window.move_timer.start(50)
        QTimer.singleShot(self.pet_window.move_duration, self.stop_movement)  # type: ignore[call-arg-type]

    def stop_movement(self):
        """停止移动"""
        if self.pet_window.is_moving:
            self.pet_window.is_moving = False
            self.pet_window.move_timer.stop()
            self.state_machine.pop_state()

import time
from typing import Dict, List, Optional, Callable
from PySide6.QtCore import QTimer, QEvent
from PySide6.QtWidgets import (
    QLabel,
)


from .base_state import (
    PetState,
    StateHandler,
    StateHandlerType,
    MenuDecoratorsType,
    GlobalMenuDecoratorsType,
)
from .normal_state_handler import NormalStateHandler
from .hungry_state_handler import HungryStateHandler
from .clicked_state_handler import ClickedStateHandler
from .dragging_state_handler import DraggingStateHandler
from .eating_state_handler import EatingStateHandler
from .moving_state_handler import MovingStateHandler
from ..system_monitor import SystemMonitor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pet_window import PetWindow


class StateMachine:
    """状态机核心类"""

    def __init__(self, pet_window: "PetWindow"):
        self.pet_window = pet_window
        self.current_state: Optional[PetState] = None
        self.state_stack: List[PetState] = [PetState.NORMAL]  # 初始状态栈不为空
        self.state_handlers: Dict[PetState, StateHandler] = {}
        self.event_handlers: Dict[QEvent.Type, List[Callable[[QEvent], bool]]] = {}
        self.ui_components: Dict[str, QLabel] = {}
        self.timers: Dict[str, QTimer] = {}

        # 网络监控初始化
        self.system_monitor = SystemMonitor(self.pet_window.config)
        self.last_net_io = self.system_monitor.get_network_usage()
        self.last_net_time = time.time()

        # 初始化所有状态处理器
        self._init_state_handlers()
        # 从正常状态开始
        self.transition_to(PetState.NORMAL)
        # 初始化系统监控定时器
        self._init_system_monitor()

    def _init_state_handlers(self):
        """初始化所有状态处理器"""
        # 使用类名映射来创建处理器实例
        handler_classes: Dict[PetState, StateHandler] = {
            PetState.NORMAL: NormalStateHandler(self),
            PetState.HUNGRY: HungryStateHandler(self),
            PetState.MOVING: MovingStateHandler(self),
            PetState.DRAGGING: DraggingStateHandler(self),
            PetState.EATING: EatingStateHandler(self),
            PetState.CLICKED: ClickedStateHandler(self),
        }

        for state, instance in handler_classes.items():
            self.register_state_handler(state, instance)
            for decorator in StateHandler.global_menu_decorators:
                if decorator["cls"] == instance.__class__:
                    decorator["cls"] = instance

    def _init_system_monitor(self):
        """初始化系统监控定时器"""
        monitor_timer = QTimer()
        monitor_timer.timeout.connect(self._update_system_info)
        monitor_timer.start(2000)
        self.timers["monitor"] = monitor_timer

    def register_state_handler(self, state: PetState, handler: StateHandler):
        """注册状态处理器"""
        self.state_handlers[state] = handler

    def register_event_handler(
        self, event_type: QEvent.Type, handler: Callable[[QEvent], bool]
    ):
        """注册事件处理器"""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def register_ui_component(self, name: str, component: QLabel):
        """注册UI组件"""
        self.ui_components[name] = component
        self.pet_window.info_layout.addWidget(component)

    def transition_to(self, new_state: PetState, is_pop: bool = False):
        """状态转换"""
        if self.current_state == new_state:
            return

        can_append_flag = True
        # 退出当前状态
        if self.current_state and self.current_state in self.state_handlers:
            res = self.state_handlers[self.current_state].on_exit()
            if res is False:
                can_append_flag = False

        # 临时状态
        special_state = [PetState.DRAGGING, PetState.EATING]
        # 非pop状态, 新状态是特殊状态, 老状态存在时: 入栈
        if (
            can_append_flag
            and not is_pop
            and new_state in special_state
            and self.current_state is not None
            and self.current_state is not PetState.NORMAL
        ):
            self.state_stack.append(self.current_state)

        # 进入新状态
        if new_state not in self.state_handlers:
            return
        res = self.state_handlers[new_state].on_enter()
        self.current_state = new_state

        if res is False:
            self.pop_state()

    def pop_state(self):
        """从堆栈弹出上一个状态"""
        if len(self.state_stack) <= 1:  # 至少保留一个正常状态
            self.transition_to(PetState.NORMAL)
            return

        previous_state = self.state_stack.pop()
        self.transition_to(previous_state, is_pop=True)

    def handle_event(self, event: QEvent) -> bool:
        """处理事件"""
        # 先处理全局事件处理器
        if event.type() in self.event_handlers:
            for handler in self.event_handlers[event.type()]:
                if handler(event):
                    return True

        # 然后交给当前状态处理器处理
        if self.current_state in self.state_handlers:
            res = self.state_handlers[self.current_state].default_handle(event)
            if res:
                return res
            return self.state_handlers[self.current_state].handle_event(event)

        return False

    def update_config(self):
        if self.current_state in self.state_handlers:
            self.state_handlers[self.current_state].update_config()

    def _update_system_info(self):
        """更新系统信息"""
        if (
            "cpu_label" not in self.ui_components
            or not self.pet_window.config.config["Info"]["ShowInfo"]
        ):
            return

        # CPU使用率
        cpu_usage = self.system_monitor.get_cpu_usage()
        self.ui_components["cpu_label"].setText(f"CPU: {cpu_usage}%")

        # 内存使用率
        memory_usage = self.system_monitor.get_memory_usage()
        self.ui_components["memory_label"].setText(f"内存: {memory_usage}%")

        # 网络速度
        current_net_io = self.system_monitor.get_network_usage()
        current_time = time.time()
        time_diff = current_time - self.last_net_time

        if time_diff > 0:
            bytes_sent = (
                current_net_io["bytes_sent"] - self.last_net_io["bytes_sent"]
            ) / time_diff
            bytes_recv = (
                current_net_io["bytes_recv"] - self.last_net_io["bytes_recv"]
            ) / time_diff
            total_speed = bytes_sent + bytes_recv

            if total_speed < 1024 * 1024:
                speed_str = f"{total_speed / 1024:.1f} KB/s"
            else:
                speed_str = f"{total_speed / (1024 * 1024):.1f} MB/s"

            self.ui_components["network_label"].setText(f"网速: {speed_str}")

        self.last_net_io = current_net_io
        self.last_net_time = current_time


__all__ = [
    "PetState",
    "StateHandlerType",
    "MenuDecoratorsType",
    "GlobalMenuDecoratorsType",
    "StateHandlerType",
    "ClickedStateHandler",
    "DraggingStateHandler",
    "EatingStateHandler",
    "HungryStateHandler",
    "MovingStateHandler",
    "NormalStateHandler",
]

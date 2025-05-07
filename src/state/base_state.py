from abc import ABC, abstractmethod
from enum import Enum, auto
from types import NoneType
from typing import List, Type, TypeVar, TypedDict
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QAction, QMouseEvent
from PySide6.QtWidgets import (
    QMenu,
)

from ..style_sheet import (
    generate_menu_css,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from state import (
        StateMachine,
    )


class PetState(Enum):
    """宠物状态枚举"""

    NORMAL = auto()  # 正常状态
    HUNGRY = auto()  # 饥饿状态
    MOVING = auto()  # 移动状态
    DRAGGING = auto()  # 拖拽状态
    EATING = auto()  # 进食状态
    CLICKED = auto()  # 点击状态


# StateHandler 的派生类
StateHandlerType = TypeVar("StateHandlerType", bound="StateHandler")


class MenuDecoratorsType(TypedDict):
    label: str
    handler: str
    separator: bool


class GlobalMenuDecoratorsType(TypedDict):
    label: str
    handler: str
    separator: bool
    cls: Type["StateHandler"] | "StateHandler"


class StateHandler(ABC):
    """状态处理器基类"""

    menu_decorators: List[MenuDecoratorsType]
    """特殊右键菜单"""
    global_menu_decorators: List[GlobalMenuDecoratorsType] = []
    """全局右键菜单"""

    def __init__(self, state_machine: "StateMachine"):
        self.state_machine = state_machine
        self.pet_window = state_machine.pet_window
        if not hasattr(self, "menu_decorators"):
            self.menu_decorators = []
        self._init_state()

    @abstractmethod
    def _init_state(self):
        """初始化状态特定的资源"""
        pass

    @abstractmethod
    def on_enter(self) -> NoneType | bool:
        """进入状态时调用(非法入栈请 `return False`)"""
        pass

    @abstractmethod
    def on_exit(self) -> NoneType | bool:
        """退出状态时调用, 返回 `False` 则表示当前状态无需入栈"""
        pass

    @abstractmethod
    def handle_event(self, event: QEvent) -> bool:
        """处理事件，返回是否已处理"""
        return False

    @abstractmethod
    def update_config(self):
        """更新配置钩子, 仅通知当前状态机, 不会触发状态切换. 正常配置应在 `on_enter` 时更新"""
        pass

    def default_handle(self, event: QEvent) -> bool:
        """默认的全局事件处理方法"""
        if isinstance(event, QMouseEvent):
            if event.type() == QEvent.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.RightButton:
                    menu = self.create_base_context_menu()
                    menu.exec(event.globalPosition().toPoint())  # type: ignore[call-arg-type]
                    return True
        return False

    def create_base_context_menu(self) -> QMenu:
        """创建右键菜单"""
        menu = QMenu(self.pet_window)
        menu.setStyleSheet(generate_menu_css())

        # 有特殊右键菜单的优先使用特殊菜单, 否则沿用全局注册的菜单
        if getattr(self.__class__, "menu_decorators", []):
            for decorator in getattr(self.__class__, "menu_decorators", []):
                if decorator["separator"]:
                    menu.addSeparator()
                try:
                    action = QAction(decorator["label"], self.pet_window)
                    if decorator["handler"]:
                        handler = getattr(self, decorator["handler"])
                        action.triggered.connect(handler)
                    menu.addAction(action)
                except Exception as e:
                    print("右键菜单错误", e)
        else:
            for decorator in StateHandler.global_menu_decorators:
                if decorator["separator"]:
                    menu.addSeparator()
                try:
                    action = QAction(decorator["label"], self.pet_window)
                    if decorator["handler"]:
                        handler = getattr(decorator["cls"], decorator["handler"])
                        action.triggered.connect(handler)
                    menu.addAction(action)
                except Exception as e:
                    print("右键菜单错误", e)

        return menu


def menu_item(
    label: str,
    handler: str,
    separator: bool = False,
    isGlobal: bool | int = False,  # 排序规则
):
    """菜单项装饰器工厂, 鼠标右键行为完全在此拦截"""

    def decorator(cls: "Type[StateHandlerType]"):
        if isGlobal is not False:
            StateHandler.global_menu_decorators.insert(
                (
                    isGlobal
                    if isGlobal < len(StateHandler.global_menu_decorators)
                    else len(StateHandler.global_menu_decorators) - 1
                ),
                {
                    "label": label,
                    "handler": handler,
                    "separator": separator,
                    "cls": cls,
                },
            )
        else:
            if not hasattr(cls, "menu_decorators"):
                cls.menu_decorators = []
            cls.menu_decorators.insert(
                0,
                {"label": label, "handler": handler, "separator": separator},
            )
        return cls

    return decorator

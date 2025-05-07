import os
from typing import Dict, List, Optional
from PySide6.QtCore import Qt, QSize, QUrl, QEvent, Signal
from PySide6.QtGui import QMovie, QIcon, QTransform
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import (
    QMainWindow,
    QLabel,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)


from .state import StateMachine, PetState
from .config import Config
from .style_sheet import generate_pet_info_css


class PetWindow(QMainWindow):
    """宠物主窗口类"""

    config_changed = Signal(str)  # 配置改变信号

    def __init__(self, config: Config):
        super().__init__()
        self.config: Config = config
        self.movie: Optional[QMovie] = None  # 当前动画
        self.movie_cache: Dict[str, QMovie] = {}

        # 初始化窗口属性
        self._setup_window()
        # 初始化UI组件
        self._setup_ui()
        # 加载资源
        self._load_resources()
        # 初始化音频
        self._setup_audio()
        # 初始化状态机
        self._setup_state_machine()
        # 立即播放初始动画
        # 设置信息窗口可见性
        self.set_info_visible()
        self.state_machine.transition_to(PetState.NORMAL)

    def _setup_window(self):
        """设置窗口属性"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 设置窗口图标
        icon_path = Config.PATH_CONFIG["Icon"]["RelativePath"]
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def _setup_ui(self):
        """初始化UI组件"""
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 动画标签
        self.animation_label = QLabel()
        self.animation_label.setFixedSize(
            self.config.config["Window"]["Width"],
            self.config.config["Window"]["Height"],
        )
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 信息窗口
        self._setup_info_widget()

        # 添加组件到布局
        self.main_layout.addWidget(self.animation_label)
        self.main_layout.addWidget(self.info_widget)

        # 更新窗口大小
        self._update_window_size()

    def _setup_info_widget(self):
        """初始化信息窗口"""
        self.info_widget = QWidget()
        self.info_widget.setFixedSize(150, 100)
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(10, 5, 10, 5)
        self.info_layout.setSpacing(2)

        # 系统信息标签
        self.cpu_label = QLabel("CPU: 0%")
        self.memory_label = QLabel("内存: 0%")
        self.network_label = QLabel("网速: 0 KB/s")

        for label in [
            self.cpu_label,
            self.memory_label,
            self.network_label,
        ]:
            self.info_layout.addWidget(label)

        self.update_theme()

    def _load_resources(self):
        """加载资源文件"""
        base_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "doro"
        )
        self._load_gif_files(base_path)

        # 鼠标交互属性
        self.setMouseTracking(True)

        # 屏幕几何信息
        self.screen_geometry = self.screen().availableGeometry()

    def _setup_audio(self):
        """初始化音频系统"""
        self.audio_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_output)

        music_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "resources", "music"
        )
        self.click_mp3_path = os.path.join(music_path, "music.mp3")

        if os.path.exists(self.click_mp3_path):
            self.audio_player.setSource(QUrl.fromLocalFile(self.click_mp3_path))
            self.audio_player.stop()

    def _setup_state_machine(self):
        """初始化状态机"""
        self.state_machine = StateMachine(self)

        self.state_machine.ui_components["cpu_label"] = self.cpu_label
        self.state_machine.ui_components["memory_label"] = self.memory_label
        self.state_machine.ui_components["network_label"] = self.network_label

    def _update_window_size(self):
        """更新窗口大小"""
        if self.config.config["Info"]["ShowInfo"]:
            total_width = (
                self.config.config["Window"]["Width"]
                + self.info_widget.width()
                + self.main_layout.spacing()
            )
        else:
            total_width = self.config.config["Window"]["Width"]
        total_height = self.config.config["Window"]["Height"]
        self.setFixedSize(total_width, total_height)

    def _load_gif_files(self, base_path: str):
        """加载GIF文件"""
        if not os.path.exists(base_path):
            print(f"路径不存在: {base_path}")
            return

        self.normal_gif_paths = self._load_gif_from_folder(
            os.path.join(base_path, "common")
        )
        self.hungry_gif_paths = self._load_gif_from_folder(
            os.path.join(base_path, "hungry")
        )
        self.move_gif_paths = self._load_gif_from_folder(
            os.path.join(base_path, "move")
        )
        self.click_gif_path = os.path.join(base_path, "click", "click.gif")
        self.eat_gif_path = os.path.join(base_path, "eat", "eat.gif")
        self.drag_gif_path = os.path.join(base_path, "drag", "drag.gif")

        for gif_path in (
            [
                self.click_gif_path,
                self.eat_gif_path,
                self.drag_gif_path,
            ]
            + self.normal_gif_paths
            + self.hungry_gif_paths
            + self.move_gif_paths
        ):
            self.movie_cache[gif_path] = QMovie(gif_path)
            self.movie_cache[gif_path].stop()

    def _load_gif_from_folder(self, folder_path: str) -> List[str]:
        """从文件夹加载GIF文件"""
        if not os.path.exists(folder_path):
            print(f"路径不存在: {folder_path}")
            return []
        return [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if f.endswith(".gif")
        ]

    # ========== 公共方法 ==========
    def play_gif(self, gif_path: str, mirror: bool = False):
        """播放GIF动画"""
        if not os.path.exists(gif_path):
            print(f"GIF文件不存在: {gif_path}")
            return

        if self.movie:
            self.movie.stop()
            self.animation_label.clear()

        movie = self.movie_cache.get(gif_path, QMovie(gif_path))
        movie.setScaledSize(
            QSize(
                self.config.config["Window"]["Width"],
                self.config.config["Window"]["Height"],
            )
        )
        self.movie = movie

        if mirror:
            # 连接帧变化信号，实现逐帧镜像
            def update_frame():
                if not self.movie:
                    return
                frame = self.movie.currentPixmap()
                mirrored = frame.transformed(QTransform().scale(-1, 1))
                self.animation_label.setPixmap(mirrored)

            self.movie.frameChanged.connect(update_frame)
            self.movie.start()
        else:
            self.animation_label.setMovie(self.movie)
            self.movie.start()

    def set_info_visible(self):
        """设置信息窗口可见性"""
        self.info_widget.setVisible(self.config.config["Info"]["ShowInfo"])
        self._update_window_size()

    def update_theme(self):
        """更新主题颜色"""
        colors = self.config.get_theme_colors()

        # 设置信息窗口样式
        self.info_widget.setStyleSheet(generate_pet_info_css(colors))
        self.info_widget.setObjectName("PetInfoWindowInfoWidget")

    def update_config(self):
        """更新配置"""
        # 更新信息框显示状态
        self.set_info_visible()

        # 更新主题
        self.update_theme()
        self.state_machine.update_config()

    # ========== 事件处理 ==========
    def event(self, event: QEvent) -> bool:
        """事件处理"""
        if hasattr(self, "state_machine") and self.state_machine.handle_event(event):
            return True
        return super().event(event)

    def closeEvent(self, event: QEvent):
        """窗口关闭事件"""
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()

        if hasattr(self, "audio_player"):
            self.audio_player.stop()
            self.audio_player.deleteLater()
        if hasattr(self, "audio_output"):
            self.audio_output.deleteLater()

        event.accept()
        os._exit(0)

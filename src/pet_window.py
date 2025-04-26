from PySide6.QtWidgets import (
    QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
)
from PySide6.QtCore import Qt, QTimer, QSize, QPoint, QUrl
from PySide6.QtGui import QMovie, QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import os
import random
import time
import psutil


class PetWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config

        # 设置窗口无边框、置顶和透明背景
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置窗口图标（favicon.ico）
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # 主窗口部件和布局
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QHBoxLayout(self.main_widget)  # 水平布局
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 信息显示部件（右侧）
        self.info_widget = QWidget()
        self.info_widget.setFixedSize(150, 100)
        self.info_layout = QVBoxLayout(self.info_widget)
        self.info_layout.setContentsMargins(10, 5, 10, 5)
        self.info_layout.setSpacing(2)

        # 系统信息标签
        self.cpu_label = QLabel("CPU: 0%")
        self.memory_label = QLabel("内存: 0%")
        self.network_label = QLabel("网速: 0 KB/s")
        for label in [self.cpu_label, self.memory_label, self.network_label]:
            self.info_layout.addWidget(label)

        # 动画显示标签（左侧）
        self.animation_label = QLabel()
        self.animation_label.setFixedSize(config.window_width, config.window_height)
        self.animation_label.setAlignment(Qt.AlignCenter)

        # 将动画和信息部件添加到主布局
        self.main_layout.addWidget(self.animation_label)
        self.main_layout.addWidget(self.info_widget)

        # 计算并设置窗口总大小
        total_width = config.window_width + self.info_widget.width() + self.main_layout.spacing()
        total_height = config.window_height
        self.setFixedSize(total_width, total_height)

        # 加载资源路径
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "doro")
        music_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "music")

        # 动画资源路径
        self.normal_gif_paths = [os.path.join(base_path, f"{i}.gif") for i in range(1, 7)]
        self.move_gif_paths = [os.path.join(base_path, f"move{i}.gif") for i in range(1, 4)]
        self.click_gif_path = os.path.join(base_path, "click.gif")
        self.click_mp3_path = os.path.join(music_path, "music.mp3")
        self.current_state = "normal"  # 当前状态：normal/move/click

        # 音频播放器初始化
        self.audio_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.audio_player.setAudioOutput(self.audio_output)

        # 加载初始动画
        self.load_gif_animation()

        # 网络监控初始化
        self.last_net_io = psutil.net_io_counters()
        self.last_net_time = time.time()

        # 系统监控定时器
        self.monitor_timer = QTimer()
        self.monitor_timer.timeout.connect(self.update_system_info)
        self.monitor_timer.start(1000)

        # 鼠标交互相关设置
        self.setMouseTracking(True)
        self.old_pos = None
        self.is_dragging = False
        self.info_visible = True

        # 宠物移动相关设置
        self.is_moving = False
        self.move_direction = None
        self.move_speed = 3
        self.move_timer = QTimer()
        self.move_timer.timeout.connect(self.move_pet)

        # 随机移动定时器
        self.random_move_timer = QTimer()
        self.random_move_timer.timeout.connect(self.start_random_movement)
        self.random_move_timer.start(5000)

        # 屏幕几何信息
        self.screen_geometry = self.screen().availableGeometry()

        # 应用主题
        self.update_theme()

    def load_gif_animation(self):
        """加载并播放随机普通状态GIF"""
        self.play_random_normal_gif()

    def play_gif(self, gif_path):
        """播放指定路径的GIF动画"""
        if not os.path.exists(gif_path):
            print(f"GIF文件不存在: {gif_path}")
            return
        self.movie = QMovie(gif_path)
        self.movie.setScaledSize(QSize(self.config.window_width, self.config.window_height))
        self.animation_label.setMovie(self.movie)
        self.movie.start()
        self.movie.finished.connect(self.return_to_normal)

    def play_random_normal_gif(self):
        """播放随机普通状态GIF"""
        if self.current_state != "normal":
            return
        gif_path = random.choice(self.normal_gif_paths)
        self.play_gif(gif_path)

    def set_info_visible(self, visible):
        """设置信息窗口可见性"""
        self.info_visible = visible
        self.info_widget.setVisible(visible)

    def update_system_info(self):
        """更新系统监控信息"""
        if not self.info_visible:
            return

        # CPU使用率
        cpu_usage = psutil.cpu_percent()

        # 内存使用率
        memory_usage = psutil.virtual_memory().percent

        # 网络速度计算
        current_net_io = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_net_time

        if time_diff > 0:
            bytes_sent = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_diff
            bytes_recv = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_diff
            total_speed = bytes_sent + bytes_recv

            # 根据速度大小选择合适的单位
            if total_speed < 1024 * 1024:
                speed_str = f"{total_speed / 1024:.1f} KB/s"
            else:
                speed_str = f"{total_speed / (1024 * 1024):.1f} MB/s"

            # 更新标签文本
            self.cpu_label.setText(f"CPU: {cpu_usage}%")
            self.memory_label.setText(f"内存: {memory_usage}%")
            self.network_label.setText(f"网速: {speed_str}")

            # 保存当前网络状态
            self.last_net_io = current_net_io
            self.last_net_time = current_time

    def update_theme(self):
        """更新主题颜色"""
        colors = self.config.get_theme_colors()

        # 设置信息窗口样式
        bg_color = colors['background']
        self.info_widget.setStyleSheet(f"""
            QWidget#PetInfoWindowInfoWidget {{
                background-color: {bg_color};
                border-radius: 10px;
                color: {colors['primary']};
                border: 1px solid {colors['border']};
            }}
            QLabel {{
                color: {colors['primary']};
                font-size: 12px;
                background-color: transparent;
                border: none;
            }}
        """)
        self.info_widget.setObjectName("PetInfoWindowInfoWidget")

    def start_random_movement(self):
        """启动随机移动"""
        if not self.is_moving and not self.is_dragging and random.random() < 0.1:
            delay = random.randint(1000, 3000)
            QTimer.singleShot(delay, self.prepare_movement)

    def prepare_movement(self):
        """准备移动动画和方向"""
        if self.is_dragging:
            return

        self.current_state = "move"
        self.play_gif(random.choice(self.move_gif_paths))

        # 随机选择移动方向
        self.move_direction = random.choice(["left", "right", "up", "down"])
        self.move_duration = random.randint(5000, 10000)
        self.is_moving = True
        self.move_timer.start(20)

        # 设置移动持续时间
        QTimer.singleShot(self.move_duration, self.stop_movement)

    def move_pet(self):
        """执行宠物移动"""
        if not self.is_moving:
            return

        current_pos = self.pos()
        new_pos = current_pos

        # 根据方向移动并处理屏幕边界
        if self.move_direction == "left":
            new_pos += QPoint(-self.move_speed, 0)
            if new_pos.x() < self.screen_geometry.left():
                self.move_direction = "right"
        elif self.move_direction == "right":
            new_pos += QPoint(self.move_speed, 0)
            if new_pos.x() > self.screen_geometry.right() - self.width():
                self.move_direction = "left"
        elif self.move_direction == "up":
            new_pos += QPoint(0, -self.move_speed)
            if new_pos.y() < self.screen_geometry.top():
                self.move_direction = "down"
        elif self.move_direction == "down":
            new_pos += QPoint(0, self.move_speed)
            if new_pos.y() > self.screen_geometry.bottom() - self.height():
                self.move_direction = "up"

        self.move(new_pos)

    def stop_movement(self):
        """停止移动"""
        self.is_moving = False
        self.move_timer.stop()
        self.return_to_normal()

    def return_to_normal(self):
        """返回普通状态"""
        self.movie.stop()
        self.current_state = "normal"
        self.play_random_normal_gif()

    def mousePressEvent(self, event):
        """鼠标按下事件处理"""
        if event.button() == Qt.LeftButton:
            # 检查是否点击在动画区域
            if self.animation_label.geometry().contains(event.position().toPoint()):
                self.old_pos = event.globalPosition().toPoint()
                self.is_dragging = True
                self.monitor_timer.stop()
                self.stop_movement()

                # 播放点击动画和音效
                self.current_state = "click"
                self.play_gif(self.click_gif_path)

                if os.path.exists(self.click_mp3_path):
                    self.audio_player.setSource(QUrl.fromLocalFile(self.click_mp3_path))
                    self.audio_player.play()

                # 18秒后返回普通状态
                QTimer.singleShot(18000, self.return_to_normal)
            else:
                super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """鼠标移动事件处理（拖动窗口）"""
        if self.old_pos and self.is_dragging:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """鼠标释放事件处理"""
        if event.button() == Qt.LeftButton and self.is_dragging:
            self.old_pos = None
            self.is_dragging = False
            self.monitor_timer.start(1000)
            # 3秒后重新启动随机移动
            QTimer.singleShot(3000, self.start_random_movement)
        else:
            super().mouseReleaseEvent(event)
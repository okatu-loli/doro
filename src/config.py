import os
from typing import Any, Dict, Literal, Optional

from .utils.FileIO import json_dump, json_load
from src.const_hint import ConfigParam, StyleSheetParam


class Config:
    # 预定义主题
    PATH_CONFIG: Dict[str, Dict[str, str]] = json_load(
        "resources/config/file_index.json"
    )
    THEMES: StyleSheetParam = json_load(PATH_CONFIG["THEME"]["RELATIVE_PATH"])

    def __init__(self):
        self._config: Optional[ConfigParam] = json_load(
            Config.PATH_CONFIG["CONFIG"]["RELATIVE_PATH"]
        )

        # 窗口配置
        self.window_width = self.config["WINDOW"].get("WINDOW_WIDTH", 200)
        self.window_height = self.config["WINDOW"].get("WINDOW_HEIGHT", 200)

        # 动画配置
        self.animation_fps = self.config["ANIMATION"].get("ANIMATION_FPS", 30)
        self.frame_delay = 1000 // self.animation_fps  # 每帧延迟（毫秒）

        # 随机切换配置
        self.random_interval = self.config["RANDOM"].get("RANDOM_INTERVAL", 5)

        # 信息框配置
        self.show_info = self.config["INFO"].get("SHOW_INFO", True)

        # 主题配置
        self.current_theme = self.config["THEME"].get("DEFAULT_THEME", "粉色主题")

        # 托盘配置
        default_ico_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources",
            "icons",
            "favicon.ico",
        )
        self.tray_icon = self.config["TRAY"].get("TRAY_ICON") or Config.PATH_CONFIG[
            "ICON"
        ].get("RELATIVE_PATH", default_ico_path)

        # 工作区配置
        self.allow_random_movement = self.config["WORKSPACE"].get(
            "ALLOW_RANDOM_MOVEMENT", True
        )

    @property
    def config(self) -> ConfigParam:
        """获取当前配置项"""
        if self._config is None:
            self._config = json_load(
                Config.PATH_CONFIG["CONFIG"]["RELATIVE_PATH"], replace=True
            )

        if self._config is None:
            self._config = self._read_default_config()
            self.save()

        return self._config

    def _read_default_config(self) -> ConfigParam:
        return json_load(
            Config.PATH_CONFIG["DEFAULT_CONFIG"]["RELATIVE_PATH"],
            replace=True,
        )

    def get_theme_colors(
        self,
    ) -> StyleSheetParam:
        """获取当前主题的颜色"""
        return StyleSheetParam(Config.THEMES.get(self.current_theme, {}))

    def get(
        self,
        key: Literal[
            "WINDOW",
            "ANIMATION",
            "RANDOM",
            "INFO",
            "THEME",
            "TRAY",
            "WORKSPACE",
        ],
    ) -> Dict[str, Any]:
        """获取配置项的值"""
        return self.config.get(key, None) or {}

    def save(self):
        json_dump(Config.PATH_CONFIG["CONFIG"]["RELATIVE_PATH"], self.config)

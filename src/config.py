from typing import Any, Dict, Final, Optional, TYPE_CHECKING


from .utils.EnvConsts import get_current_location

from .utils.FileIO import json_dump, json_load
from .auto_typehint import ConfigHint, FileIndexHint, ThemeHint

if TYPE_CHECKING:
    from .MainLayer import MainLayer


class Config:
    # 预定义主题
    PATH_CONFIG: FileIndexHint.FileIndexParam = json_load(
        get_current_location() + "/resources/config/file_index.json"
    )
    THEMES: ThemeHint.ThemeParam = json_load(PATH_CONFIG["Theme"]["RelativePath"])

    def __init__(self, main_layer: "MainLayer"):
        self.main_layer: MainLayer = main_layer

        _config: Optional[ConfigHint.ConfigParam] = json_load(
            Config.PATH_CONFIG["Config"]["RelativePath"]
        )
        self._default_config: Final[ConfigHint.ConfigParam] = (
            self._read_default_config()
        )

        self._config: ConfigHint.ConfigParam = _config or self._default_config
        if _config is None:
            self.save()

    @property
    def config(self) -> ConfigHint.ConfigParam:
        """获取当前配置项"""
        for key, value in self._default_config.items():
            if key not in self._config:
                self._config[key] = value

        return self._config

    def _read_default_config(self) -> ConfigHint.ConfigParam:
        return json_load(
            Config.PATH_CONFIG["DefaultConfig"]["RelativePath"],
            replace=True,
        )

    def get_theme_colors(
        self,
    ) -> ThemeHint.ThemeParam:
        """获取当前主题的颜色"""
        return ThemeHint.ThemeParam(
            Config.THEMES.get(self.config["Theme"]["DefaultTheme"], {})
        )

    def get(self, key: ConfigHint.ConfigLiteral) -> Dict[str, Any]:
        """获取配置项的值"""
        return self.config.get(key, None) or {}

    def save(self):
        json_dump(Config.PATH_CONFIG["Config"]["RelativePath"], self.config)

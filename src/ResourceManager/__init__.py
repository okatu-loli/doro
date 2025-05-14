from functools import cache
import os
from typing import Any, Dict, List, TYPE_CHECKING


from ..auto_typehint import FileIndexHint, MusicHint, GifHint

if TYPE_CHECKING:
    from ..MainLayer import MainLayer


def load_files(resource_dict: Any) -> Dict[str, List[str]]:
    return {
        key: [
            os.path.join(str(path), file)
            for file in os.listdir(str(path))
            if os.path.isfile(os.path.join(str(path), file))
        ]
        for key, path in resource_dict.items()
    }


class ResourceManager:
    def __init__(self, config: FileIndexHint.ResourcesParam, main_layer: "MainLayer"):
        self._main_layer: MainLayer = main_layer
        self._resource_config: FileIndexHint.ResourcesParam = config
        self._music = load_files(self._resource_config.get("Music", {}))
        self._gif = load_files(self._resource_config.get("Gif", {}))

    @cache
    def get_gif(self, key: GifHint.GifDirLiteral) -> List[str]:
        """获取gif资源"""
        return self._gif.get(key, [])

    @cache
    def get_all_gif(self) -> List[str]:
        return [file for files in self._gif.values() for file in files]

    @cache
    def get_music(self, key: MusicHint.MusicDirLiteral) -> List[str]:
        """获取音乐资源"""
        return self._music.get(key, [])

    @cache
    def get_all_music(self) -> List[str]:
        return [file for files in self._music.values() for file in files]


__all__ = [
    "ResourceManager",
]

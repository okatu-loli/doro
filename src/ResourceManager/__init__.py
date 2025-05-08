import os
from typing import Any, Dict, List, Union
from ..auto_typehint import FileIndexHint, MusicHint, GifHint


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
    def __init__(self, config: FileIndexHint.ResourcesParam):
        self._resource_config: FileIndexHint.ResourcesParam = config
        self._music = load_files(self._resource_config.get("Music", {}))
        self._gif = load_files(self._resource_config.get("Gif", {}))

    def get_music(self, key: MusicHint.MusicDirLiteral) -> Union[Any, List[str]]:
        """获取音乐资源"""
        return self._music.get(key, [])

    def get_gif(self, key: GifHint.GifDirLiteral) -> Union[Any, List[str]]:
        """获取gif资源"""
        return self._gif.get(key, [])


__all__ = [
    "ResourceManager",
]

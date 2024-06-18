from pathlib import Path

from src.const.types import FileStringOrPath


def file_resolve_path(path: FileStringOrPath) -> Path:
    return path if path is Path else Path(path)

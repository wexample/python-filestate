from __future__ import annotations

from typing import Optional

from typing_extensions import TypedDict


class StateItemConfig(TypedDict):
    name: str
    children: Optional[any]


class FileSystemStructurePermission(TypedDict):
    mode: int
    recursive: bool

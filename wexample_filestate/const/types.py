from __future__ import annotations

from typing import Optional, List

from typing_extensions import TypedDict


class StateItemConfig(TypedDict, total=False):
    name: str
    mode: int | FileSystemStructurePermission
    children: Optional[List[StateItemConfig]]


class FileSystemStructurePermission(TypedDict):
    mode: int
    recursive: bool

from __future__ import annotations

from typing import Optional, List
from typing_extensions import TypedDict


class StateItemConfig(TypedDict, total=False):
    name: str
    type: Optional[str]
    mode: Optional[FileSystemPermission]
    children: Optional[List[StateItemConfig]]


class FileSystemPermissionConfig(TypedDict):
    mode: int
    recursive: bool


FileSystemPermission = FileSystemPermissionConfig | str | int

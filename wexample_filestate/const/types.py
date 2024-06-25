from __future__ import annotations

from typing import Optional, List
from typing_extensions import TypedDict


class StateItemConfig(TypedDict, total=False):
    name: str
    type: Optional[str]
    mode: Optional[FileSystemPermission]
    children: Optional[List[StateItemConfig]]
    remove_backup_max_file_size: Optional[int]
    should_exist: Optional[bool]


class FileSystemPermissionConfig(TypedDict):
    mode: int
    recursive: bool


FileSystemPermission = FileSystemPermissionConfig | str | int

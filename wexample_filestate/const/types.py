from __future__ import annotations
from typing import Optional, List, Literal
from typing_extensions import TypedDict
from wexample_filestate.const.enums import DiskItemType


class StateItemConfig(TypedDict, total=False):
    name: Optional[str]
    name_pattern: Optional[str]
    type: Optional[Literal[DiskItemType.FILE, DiskItemType.DIRECTORY]]
    mode: Optional[FileSystemPermission]
    children: Optional[List[StateItemConfig]]
    remove_backup_max_file_size: Optional[int]
    should_exist: Optional[bool]


class FileSystemPermissionConfig(TypedDict):
    mode: int
    recursive: bool


FileSystemPermission = FileSystemPermissionConfig | str | int

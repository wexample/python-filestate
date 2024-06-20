from __future__ import annotations

from typing import Optional, TYPE_CHECKING, Union, List

from typing_extensions import TypedDict

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

# These notations make imports as used.
TargetFileOrDirectory = Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]


class StateItemConfig(TypedDict, total=False):
    name: str
    type: Optional[str]
    mode: Optional[int | FileSystemStructurePermission]
    children: Optional[List[StateItemConfig]]


class FileSystemStructurePermission(TypedDict):
    mode: int
    recursive: bool

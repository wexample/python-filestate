from __future__ import annotations

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
    from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource

TargetFileOrDirectory = Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]
SourceFileOrDirectory = Union["FileStateItemDirectorySource", "FileStateItemFileSource"]

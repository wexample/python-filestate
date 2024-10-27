from __future__ import annotations

from typing import Union, TYPE_CHECKING

from wexample_helpers.helpers.import_helper import import_dummy

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

    import_dummy(FileStateItemDirectoryTarget)

TargetFileOrDirectory = Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]
SourceFileOrDirectory = Union["FileStateItemDirectorySource", "FileStateItemFileSource"]

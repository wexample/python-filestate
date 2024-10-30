from __future__ import annotations

from typing import TYPE_CHECKING, Union

from wexample_helpers.helpers.import_helper import import_dummy

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import \
        FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import \
        FileStateItemFileTarget

    import_dummy(FileStateItemFileTarget)
    import_dummy(FileStateItemDirectoryTarget)

TargetFileOrDirectory = Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]

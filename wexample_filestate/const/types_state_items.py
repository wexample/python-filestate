from __future__ import annotations

from typing import TYPE_CHECKING, Union

from wexample_helpers.helpers.import_helper import import_dummy

if TYPE_CHECKING:
    from wexample_filestate.item.item_source_directory import (
        ItemSourceDirectory,
    )
    from wexample_filestate.item.item_target_directory import (
        ItemTargetDirectory,
    )
    from wexample_filestate.item.item_source_file import (
        ItemSourceFile,
    )
    from wexample_filestate.item.item_target_file import (
        ItemTargetFile,
    )

    import_dummy(ItemTargetFile)
    import_dummy(ItemTargetDirectory)
    import_dummy(ItemSourceFile)
    import_dummy(ItemSourceDirectory)

TargetFileOrDirectoryType = Union["ItemTargetDirectory", "ItemTargetFile"]
SourceFileOrDirectoryType = Union["ItemSourceDirectory", "ItemTargetSource"]

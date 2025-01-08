from __future__ import annotations

from typing import TYPE_CHECKING, Union

from wexample_helpers.helpers.polyfill import polyfill_import

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

    polyfill_import(ItemTargetFile)
    polyfill_import(ItemTargetDirectory)
    polyfill_import(ItemSourceFile)
    polyfill_import(ItemSourceDirectory)

TargetFileOrDirectoryType = Union["ItemTargetDirectory", "ItemTargetFile"]
SourceFileOrDirectoryType = Union["ItemSourceDirectory", "ItemTargetSource"]

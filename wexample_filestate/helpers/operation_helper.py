from __future__ import annotations

from typing import List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


def operation_list_all() -> List[Type["AbstractOperation"]]:
    from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
    from wexample_filestate.operation.file_create_operation import FileCreateOperation
    from wexample_filestate.operation.file_remove_operation import FileRemoveOperation

    return [
        FileCreateOperation,
        FileRemoveOperation,
        ItemChangeModeOperation,
    ]

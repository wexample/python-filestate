from typing import List, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


def operation_list_all() -> List[Type["AbstractOperation"]]:
    from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation

    return [
        ItemChangeModeOperation,
    ]

from typing import List, Type, TYPE_CHECKING
from wexample_filestate.operations_provider.abstract_operations_provider import AbstractOperationsProvider

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class DefaultOperationsProvider(AbstractOperationsProvider):
    @staticmethod
    def get_operations() -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
        from wexample_filestate.operation.file_create_operation import FileCreateOperation
        from wexample_filestate.operation.file_remove_operation import FileRemoveOperation
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        return [
            FileCreateOperation,
            FileRemoveOperation,
            FileWriteOperation,
            ItemChangeModeOperation
        ]

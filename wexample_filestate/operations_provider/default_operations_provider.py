from typing import List, Type
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.file_create_operation import FileCreateOperation
from wexample_filestate.operations_provider.abstract_operations_provider import AbstractOperationsProvider


class DefaultOperationsProvider(AbstractOperationsProvider):
    @staticmethod
    def get_operations() -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation

        return [
            FileCreateOperation,
            ItemChangeModeOperation
        ]

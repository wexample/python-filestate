from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operations_provider.abstract_operations_provider import (
    AbstractOperationsProvider,
)

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class DefaultOperationsProvider(AbstractOperationsProvider):
    @staticmethod
    def get_operations() -> list[type[AbstractOperation]]:
        from wexample_filestate.operation.file_create_operation import (
            FileCreateOperation,
        )
        from wexample_filestate.operation.file_remove_operation import (
            FileRemoveOperation,
        )
        from wexample_filestate.operation.file_write_operation import FileWriteOperation
        from wexample_filestate.operation.file_change_mode_operation import (
            FileChangeModeOperation,
        )

        return [
            # filestate: python-iterable-sort
            FileChangeModeOperation,
            FileCreateOperation,
            FileRemoveOperation,
            FileWriteOperation,
        ]
from __future__ import annotations

import os
from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class FileRenameOperation(FileManipulationOperationMixin, AbstractOperation):
    def __init__(self, target, new_name: str, description: str | None = None) -> None:
        super().__init__(target=target, description=description)
        self.new_name = new_name

    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.LOCATION

    def apply(self) -> None:
        self._backup_target_file()
        
        old_path = self._original_path
        new_path = old_path.parent / self.new_name
        
        os.rename(old_path, new_path)

    def undo(self) -> None:
        self._restore_target_file()

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class FileRemoveOperation(FileManipulationOperationMixin, AbstractOperation):
    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.LOCATION

    def apply(self) -> None:
        self._backup_target_file()

        if self.target.is_file():
            os.remove(self._original_path)
        elif self.target.is_directory():
            shutil.rmtree(self._original_path)

    def describe_after(self) -> str:
        path = self.target.get_path().as_posix()
        return f"'{path}' has been removed as requested by configuration."

    def describe_before(self) -> str:
        path = self.target.get_path().as_posix()
        kind = "directory" if self.target.is_directory() else "file"
        return f"The {kind} '{path}' exists but is configured to be absent. It will be removed."

    def description(self) -> str:
        return "Remove a file or directory that should not exist according to configuration."

    def undo(self) -> None:
        self._restore_target_file()

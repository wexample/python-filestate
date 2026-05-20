from __future__ import annotations

import shutil
from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.operation.abstract_file_manipulation_operation import (
    AbstractFileManipulationOperation,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


@base_class
class FileRemoveOperation(AbstractFileManipulationOperation):
    @classmethod
    def get_scopes(cls) -> [Scope]:
        from wexample_filestate.enum.scopes import Scope

        return [Scope.LOCATION]

    def apply_operation(self) -> None:
        self._backup_target_file()

        if self.target.is_file():
            self.target.get_local_file().remove()
        elif self.target.is_directory():
            shutil.rmtree(self._original_path)

    def undo(self) -> None:
        self._restore_target_file()

from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import (
        FileStateItemDirectoryTarget,
    )
    from wexample_filestate.item.file_state_item_file_target import (
        FileStateItemFileTarget,
    )


class FileRemoveOperation(FileManipulationOperationMixin, AbstractOperation):
    @staticmethod
    def applicable(
        target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]
    ) -> bool:
        if (
            target.source
            and not FileManipulationOperationMixin.option_should_exist_is_true(target)
        ):
            return True

        return False

    def describe_before(self) -> str:
        return "EXISTS"

    def describe_after(self) -> str:
        return "REMOVED"

    def description(self) -> str:
        return "Remove existing file"

    def apply(self) -> None:
        self._backup_target_file()

        if self.target.is_file():
            os.remove(self._original_path_str)
        elif self.target.is_directory():
            shutil.rmtree(self._original_path_str)

    def undo(self) -> None:
        self._restore_target_file()

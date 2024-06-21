from __future__ import annotations

import os
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_touch

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class FileCreateOperation(AbstractOperation):
    _original_path_str: str

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if not target.source:
            return True

        return False

    def describe_before(self) -> str:
        return 'MISSING'

    def describe_after(self) -> str:
        return 'CREATED'

    def description(self) -> str:
        return 'Create missing file'

    def apply(self) -> None:
        self._original_path_str = self.target.path.resolve().as_posix()
        file_touch(self._original_path_str)

    def undo(self) -> None:
        os.remove(self._original_path_str)

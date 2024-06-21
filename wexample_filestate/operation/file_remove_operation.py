from __future__ import annotations

import os
import shutil
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_read, file_write

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class FileRemoveOperation(AbstractOperation):
    _original_path_str: str
    _original_file_mode: int
    _original_file_content: str = ''

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source and target.should_exist is False:
            return True

        return False

    def describe_before(self) -> str:
        return 'EXISTS'

    def describe_after(self) -> str:
        return 'REMOVED'

    def description(self) -> str:
        return 'Remove existing file'

    def apply(self) -> None:
        self._original_path_str = self.get_target_file_path()
        self._original_file_mode = self.target.path.stat().st_mode
        file_path = self.get_target_file_path()
        size = os.path.getsize(file_path)

        # Save content if not too large.
        if size < self.target.remove_backup_max_file_size:
            self._original_file_content = file_read(file_path)

        if self.target.is_file():
            os.remove(self._original_path_str)
        elif self.target.is_directory():
            shutil.rmtree(self._original_path_str)

    def undo(self) -> None:
        if self.target.is_file():
            file_write(self._original_path_str, self._original_file_content)
            os.chmod(self._original_path_str, self._original_file_mode)
        elif self.target.is_directory():
            os.mkdir(self._original_path_str)

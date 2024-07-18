from __future__ import annotations

import os
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.options.default_content_option import DefaultContentOption
from wexample_helpers.helpers.file_helper import file_touch, file_write

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class FileCreateOperation(AbstractOperation):
    _original_path_str: str

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        from wexample_filestate.options.should_exist_option import ShouldExistOption

        if not target.source and target.get_option_value(ShouldExistOption) is True:
            return True

        return False

    def describe_before(self) -> str:
        return 'MISSING'

    def describe_after(self) -> str:
        return 'CREATED'

    def description(self) -> str:
        return 'Create missing file'

    def apply(self) -> None:
        self._original_path_str = self.get_target_file_path()
        if self.target.is_file():
            content = self.target.get_option_value(DefaultContentOption)

            if content:
                if isinstance(content, str):
                    str_content = content
                else:
                    str_content = content.render(self.target, current_value='')

                file_write(self._original_path_str, str_content)
            else:
                file_touch(self._original_path_str)

        elif self.target.is_directory():
            os.mkdir(self._original_path_str)

    def undo(self) -> None:
        if self.target.is_file():
            os.remove(self._original_path_str)
        elif self.target.is_directory():
            # Do not remove recursively, as for now it only can be created empty with mkdir.
            os.rmdir(self._original_path_str)

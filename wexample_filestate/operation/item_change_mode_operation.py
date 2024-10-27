from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional, cast

from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_validate_mode_octal_or_fail, \
    file_path_get_mode_num

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: Optional[str] = None

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            from wexample_filestate.option.mode_option import ModeOption

            option = cast(ModeOption, target.get_option(ModeOption))
            if option:
                file_validate_mode_octal_or_fail(option.get_octal())

                if file_path_get_mode_num(target.source.path) != option.get_int():
                    return True

        return False

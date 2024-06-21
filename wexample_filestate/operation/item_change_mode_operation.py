from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num, file_validate_mode_octal_or_fail, \
    file_mode_num_to_octal, file_change_mode_recursive

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation, ABC):

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            if target.mode:
                file_validate_mode_octal_or_fail(target.get_octal_mode())

                if target.source.path.stat().st_mode != target.get_int_mode():
                    return True

        return False

    def describe_before(self) -> str:
        return file_mode_num_to_octal(self.target.source.path.stat().st_mode)

    def describe_after(self) -> str:
        return self.target.mode

    def description(self) -> str:
        return 'Change file permission'

    def apply(self) -> None:
        print(self.target.get_octal_mode())
        print(self.target.get_int_mode())
        print(0o777)
        file_change_mode_recursive(
            self.target.source.path,
            self.target.get_int_mode()
        )
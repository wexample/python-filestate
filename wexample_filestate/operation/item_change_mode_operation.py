from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num, file_validate_mode_octal_or_fail, \
    file_change_mode_recursive

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: Optional[str] = None

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            if target.mode:
                file_validate_mode_octal_or_fail(target.get_octal_mode())

                if target.source.path.stat().st_mode != target.get_int_mode():
                    return True

        return False

    def describe_before(self) -> str:
        return self.target.source.get_octal_mode()

    def describe_after(self) -> str:
        return self.target.mode

    def description(self) -> str:
        return 'Change file permission'

    def apply(self) -> None:
        self._original_octal_mode = self.target.source.get_octal_mode()
        file_change_mode_recursive(
            self.target.source.path,
            self.target.get_int_mode()
        )

    def undo(self) -> None:
        file_change_mode_recursive(
            self.target.source.path,
            file_mode_octal_to_num(self._original_octal_mode)
        )

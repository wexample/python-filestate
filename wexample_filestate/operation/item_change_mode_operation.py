from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional, cast

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.options.mode_option import ModeOption
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num, file_validate_mode_octal_or_fail, \
    file_change_mode_recursive, file_change_mode, file_path_get_mode_num

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: Optional[str] = None

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            from wexample_filestate.options.mode_option import ModeOption

            option = cast(ModeOption, target.get_option(ModeOption))
            if option:
                file_validate_mode_octal_or_fail(option.get_octal())

                if file_path_get_mode_num(target.source.path) != option.get_int():
                    return True

        return False

    def describe_before(self) -> str:
        return self.target.source.get_octal_mode()

    def describe_after(self) -> str:
        return self.target.get_option_value(ModeOption)

    def description(self) -> str:
        return 'Change file permission'

    def apply(self) -> None:
        from wexample_filestate.options.mode_option import ModeOption
        from wexample_filestate.options.mode_recursive_option import ModeRecursiveOption

        self._original_octal_mode = self.target.source.get_octal_mode()
        mode_int = cast(ModeOption, self.target.get_option(ModeOption)).get_int()

        if self.target.get_option_value(ModeRecursiveOption) is True:
            file_change_mode(
                self.target.source.path,
                mode_int
            )
        else:
            file_change_mode_recursive(
                self.target.source.path,
                mode_int
            )

    def undo(self) -> None:
        file_change_mode_recursive(
            self.target.source.path,
            file_mode_octal_to_num(self._original_octal_mode)
        )

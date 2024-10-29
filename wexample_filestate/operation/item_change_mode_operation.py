from __future__ import annotations

from typing import TYPE_CHECKING, Union, Optional, cast

from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.mode_config_option import ModeConfigOption
from wexample_helpers.helpers.file_helper import file_validate_mode_octal_or_fail, \
    file_path_get_mode_num, file_change_mode_recursive, file_change_mode, file_mode_octal_to_num

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation):
    _original_octal_mode: Optional[str] = None

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            from wexample_filestate.option.mode_config_option import ModeConfigOption

            option = cast(ModeConfigOption, target.get_option(ModeConfigOption))
            if option:
                file_validate_mode_octal_or_fail(option.get_octal())

                if file_path_get_mode_num(target.source.path) != option.get_int():
                    return True

        return False

    def describe_before(self) -> str:
        return self.target.source.get_octal_mode()

    def describe_after(self) -> str:
        return self.target.get_option(ModeConfigOption).value.get_str()

    def description(self) -> str:
        return 'Change file permission'

    def apply(self) -> None:
        from wexample_filestate.option.mode_recursive_config_option import ModeRecursiveConfigOption

        self._original_octal_mode = self.target.source.get_octal_mode()
        mode_int = cast(ModeConfigOption, self.target.get_option(ModeConfigOption)).get_int()
        mode_recursive_option = self.target.get_option(ModeRecursiveConfigOption)

        if mode_recursive_option and mode_recursive_option.value.get_bool() is True:
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

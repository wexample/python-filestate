from abc import ABC
from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num, file_validate_mode_octal_or_fail, \
    file_mode_num_to_octal

if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
    from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget


class ItemChangeModeOperation(AbstractOperation, ABC):

    @staticmethod
    def applicable(target: Union["FileStateItemDirectoryTarget", "FileStateItemFileTarget"]) -> bool:
        if target.source:
            if target.mode:
                file_validate_mode_octal_or_fail(target.mode)

                if target.source.path.stat().st_mode != file_mode_octal_to_num(target.mode):
                    return True

        return False

    def to_tty(self) -> str:
        return (f'Current source file mode {file_mode_num_to_octal(self.target.source.path.stat().st_mode)} '
                f'will be changed by mode {self.target.mode}')

    def apply(self) -> None:
        pass

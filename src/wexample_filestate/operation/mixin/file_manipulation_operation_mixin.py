from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.const.types import PathOrString

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_helpers.const.types import PathOrString


class FileManipulationOperationMixin(AbstractOperation):
    _original_file_content: str = ""
    _original_file_mode: int
    _original_path: PathOrString

    @staticmethod
    def option_should_exist_is_true(target: TargetFileOrDirectoryType) -> bool:
        from wexample_filestate.option.should_exist_option import (
            ShouldExistOption,
        )

        return target.get_option_value(ShouldExistOption, default=True).is_true()

    def _backup_file_content(
        self, target: TargetFileOrDirectoryType, file_path: PathOrString
    ) -> bool:
        import os

        from wexample_filestate.option.remove_backup_max_file_size_option import (
            REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            RemoveBackupMaxFileSizeOption,
        )
        from wexample_helpers.helpers.file import file_read

        size = os.path.getsize(file_path)

        # Save content if not too large.
        if size < int(
            target.get_option_value(
                RemoveBackupMaxFileSizeOption,
                default=REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            ).get_int()
        ):
            self._original_file_content = file_read(file_path)

            return True
        return False

    def _backup_target_file(self) -> None:
        self._original_path = self.target.get_path()
        self._original_file_mode = self.target.get_path().stat().st_mode

        self._backup_file_content(
            target=self.target,
            file_path=self._original_path,
        )

    def _restore_target_file(self) -> None:
        import os

        from wexample_helpers.helpers.file import file_write

        if self.target.is_file():
            file_write(self._original_path, self._original_file_content)
            os.chmod(self._original_path, self._original_file_mode)
        elif self.target.is_directory():
            os.mkdir(self._original_path)

    def _target_file_write(self, content: str) -> None:
        self._backup_target_file()
        self.target.get_local_file().write(content=content)

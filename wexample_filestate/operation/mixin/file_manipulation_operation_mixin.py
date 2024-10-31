from typing import TYPE_CHECKING, Union

from wexample_filestate.operation.abstract_operation import AbstractOperation

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class FileManipulationOperationMixin(AbstractOperation):
    _original_path_str: str
    _original_file_mode: int
    _original_file_content: str = ""

    def _get_target_file_path(self, target: "TargetFileOrDirectory") -> str:
        return target.get_resolved()

    def _backup_target_file(self) -> None:
        self._original_path_str = self._get_target_file_path(target=self.target)
        assert self.target.path is not None
        self._original_file_mode = self.target.path.stat().st_mode

        self._backup_file_content(
            target=self.target,
            file_path=self._get_target_file_path(target=self.target),
        )

    def _restore_target_file(self) -> None:
        import os

        from wexample_helpers.helpers.file_helper import file_write

        if self.target.is_file():
            file_write(self._original_path_str, self._original_file_content)
            os.chmod(self._original_path_str, self._original_file_mode)
        elif self.target.is_directory():
            os.mkdir(self._original_path_str)

    def _backup_file_content(
        self, target: "TargetFileOrDirectory", file_path: str
    ) -> bool:
        import os

        from wexample_filestate.config_option.remove_backup_max_file_size_config_option import (
            REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            RemoveBackupMaxFileSizeConfigOption,
        )
        from wexample_helpers.helpers.file_helper import file_read

        size = os.path.getsize(file_path)

        # Save content if not too large.
        if size < int(
            target.get_option_value(
                RemoveBackupMaxFileSizeConfigOption,
                default=REMOVE_BACKUP_MAX_FILE_SIZE_DEFAULT,
            ).get_int()
        ):
            self._original_file_content = file_read(file_path)

            return True
        return False

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.config_option.content_config_option import ContentConfigOption
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)
from wexample_helpers.helpers.file_helper import file_read, file_write

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class FileWriteOperation(FileManipulationOperationMixin, AbstractOperation):
    @staticmethod
    def applicable(target: "TargetFileOrDirectoryType") -> bool:
        from wexample_filestate.config_option.content_config_option import (
            ContentConfigOption,
        )

        if target.get_option(ContentConfigOption) is not None:
            current_content = file_read(target.get_resolved())
            new_content = target.get_option_value(ContentConfigOption).get_str()

            return current_content != new_content

        return False

    def describe_before(self) -> str:
        return "CURRENT_CONTENT"

    def describe_after(self) -> str:
        return "REWRITTEN_CONTENT"

    def description(self) -> str:
        return "Regenerate file content"

    def _target_file_write(self, content: str):
        self._backup_target_file()
        file_path = self._get_target_file_path(target=self.target)
        file_write(file_path, content=content)

    def apply(self) -> None:
        self._target_file_write(
            content=self.target.get_option_value(ContentConfigOption).get_str()
        )

    def undo(self) -> None:
        self._restore_target_file()

from __future__ import annotations

from typing import TYPE_CHECKING
import os

from wexample_filestate.config_option.content_config_option import ContentConfigOption
from wexample_filestate.config_option.should_contain_lines_config_option import ShouldContainLinesConfigOption
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)
from wexample_helpers.helpers.file import file_read, file_write

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class FileWriteOperation(FileManipulationOperationMixin, AbstractOperation):
    @staticmethod
    def applicable(target: "TargetFileOrDirectoryType") -> bool:
        content_option = target.get_option(ContentConfigOption)
        should_contain_lines_option = target.get_option(ShouldContainLinesConfigOption)

        if content_option is not None:
            current_content = file_read(target.get_resolved()) if os.path.exists(target.get_resolved()) else ""
            new_content = target.get_option_value(ContentConfigOption).get_str()
            return current_content != new_content

        if should_contain_lines_option is not None:
            required_lines = target.get_option_value(ShouldContainLinesConfigOption)
            if not os.path.exists(target.get_resolved()):
                return True
            current_content = file_read(target.get_resolved())
            current_lines = current_content.splitlines()
            return any(line not in current_lines for line in required_lines)

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
        content_option = self.target.get_option(ContentConfigOption)
        should_contain_lines_option = self.target.get_option(ShouldContainLinesConfigOption)

        if content_option is not None:
            self._target_file_write(
                content=self.target.get_option_value(ContentConfigOption).get_str()
            )
        elif should_contain_lines_option is not None:
            required_lines = self.target.get_option_value(ShouldContainLinesConfigOption)
            current_content = file_read(self._get_target_file_path(self.target)) if os.path.exists(self._get_target_file_path(self.target)) else ""
            current_lines = current_content.splitlines()

            # Add missing lines
            lines_to_add = [line for line in required_lines if line not in current_lines]
            if lines_to_add:
                new_content = current_content
                if new_content and not new_content.endswith('\n'):
                    new_content += '\n'
                new_content += '\n'.join(lines_to_add)
                self._target_file_write(content=new_content)

    def undo(self) -> None:
        self._restore_target_file()

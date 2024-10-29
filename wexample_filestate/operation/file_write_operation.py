from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import FileManipulationMixin
from wexample_filestate.option.content_option import ContentOption
from wexample_helpers.helpers.file_helper import file_write, file_read

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class FileWriteOperation(FileManipulationMixin, AbstractOperation):
    @staticmethod
    def applicable(target: "TargetFileOrDirectory") -> bool:
        from wexample_filestate.option.content_option import ContentOption

        if target.get_option(ContentOption) is not None:
            current_content = file_read(target.path.resolve().as_posix())
            new_content = FileWriteOperation._render_new_content(target)

            return current_content != new_content

        return False

    @staticmethod
    def _render_new_content(target: "TargetFileOrDirectory") -> str:
        return target.get_option_value(ContentOption).render()

    def describe_before(self) -> str:
        return 'CURRENT_CONTENT'

    def describe_after(self) -> str:
        return 'REWRITTEN_CONTENT'

    def description(self) -> str:
        return 'Regenerate file content'

    def apply(self) -> None:
        file_path = self._get_target_file_path(target=self.target)
        self._backup_target_file()

        file_write(file_path, FileWriteOperation._render_new_content(self.target))

    def undo(self) -> None:
        self._restore_target_file()

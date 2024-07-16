from __future__ import annotations

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_helpers.helpers.file_helper import file_write, file_read


class FileWriteOperation(AbstractOperation):
    _original_file_content: str

    @staticmethod
    def applicable(target: TargetFileOrDirectory) -> bool:
        from wexample_filestate.options.content_option import ContentOption

        if target.get_option(ContentOption) is not None:
            return True

        return False

    def describe_before(self) -> str:
        return 'CURRENT_CONTENT'

    def describe_after(self) -> str:
        return 'REWRITTEN_CONTENT'

    def description(self) -> str:
        return 'Regenerate file content'

    def apply(self) -> None:
        from wexample_filestate.options.content_option import ContentOption

        file_path = self.get_target_file_path()
        self._original_file_content = file_read(file_path)
        content = self.target.get_option_value(ContentOption)

        if isinstance(content, str):
            str_content = content
        else:
            str_content = content.render(self.target, self._original_file_content)

        file_write(file_path, str_content)

    def undo(self) -> None:
        file_write(
            self.get_target_file_path(),
            self._original_file_content
        )

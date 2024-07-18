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
            current_content, new_content = FileWriteOperation.get_current_and_new_contents(target)
            return current_content != new_content

        return False

    @staticmethod
    def get_current_and_new_contents(target: TargetFileOrDirectory):
        from wexample_filestate.options.content_option import ContentOption

        current_content = file_read(target.path.resolve().as_posix())

        content = target.get_option_value(ContentOption)
        if isinstance(content, str):
            new_content = content
            current_content, new_content = FileWriteOperation.get_current_and_new_contents(target)
            return current_content != new_content
        else:
            new_content = content.render(target, current_content)

        return current_content, new_content

    def describe_before(self) -> str:
        return 'CURRENT_CONTENT'

    def describe_after(self) -> str:
        return 'REWRITTEN_CONTENT'

    def description(self) -> str:
        return 'Regenerate file content'

    def apply(self) -> None:
        file_path = self.get_target_file_path()
        current_content, new_content = FileWriteOperation.get_current_and_new_contents(target)

        file_write(file_path, new_content)

    def undo(self) -> None:
        file_write(
            self.get_target_file_path(),
            self._original_file_content
        )

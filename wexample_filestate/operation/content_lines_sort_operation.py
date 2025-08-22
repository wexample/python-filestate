from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.config_option.content_options_config_option import (
    ContentOptionsConfigOption,
)
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ContentLinesSortOperation(FileManipulationOperationMixin, AbstractOperation):
    """Sort file content lines alphabetically (lexicographic order).

    Triggered by: { "content_options": ["lines_sort"] }
    """

    @classmethod
    def get_scope(cls) -> Scope:
        return Scope.CONTENT

    @classmethod
    def applicable_option(
        cls, target: TargetFileOrDirectoryType, option: AbstractConfigOption
    ) -> bool:
        if not isinstance(option, ContentOptionsConfigOption):
            return False

        value = option.get_value()
        if value is None or not value.has_item_in_list(
            ContentOptionsConfigOption.OPTION_NAME_LINES_SORT
        ):
            return False

        local_file = target.get_local_file()
        if not target.is_file() or not local_file.path.exists():
            # If the file doesn't exist, nothing to sort yet.
            return False

        src = local_file.read()
        sorted_src = cls._sorted_lines_content(src)
        return sorted_src != src

    @staticmethod
    def _sorted_lines_content(src: str) -> str:
        # Preserve a trailing newline if it exists
        had_trailing_newline = src.endswith("\n")
        lines = src.splitlines()
        lines.sort()  # default lexicographic sort, case-sensitive
        out = "\n".join(lines)
        if had_trailing_newline:
            out += "\n"
        return out

    def apply(self) -> None:
        src = self.target.get_local_file().read()
        updated = self._sorted_lines_content(src)
        if updated != src:
            self._target_file_write(content=updated)

    def undo(self) -> None:
        self._restore_target_file()

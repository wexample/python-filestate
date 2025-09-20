from __future__ import annotations

from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.option.content.abstract_content_child_option import AbstractContentChildOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class SortLinesOption(AbstractContentChildOption):
    def get_description(self) -> str:
        return "Sort file content lines alphabetically"

    def create_required_operation(
            self, target: TargetFileOrDirectoryType
    ) -> AbstractOperation | None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if self.get_value().is_true():
            base_content = self._get_base_content(target)
            if base_content is not None:
                sorted_content = self._sort_lines_content(base_content)
                current_content = self._read_current_content(target) or ""
                
                if sorted_content != current_content:
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=sorted_content,
                        description=self.get_description(),
                    )

        return None

    def _sort_lines_content(self, content: str) -> str:
        """Sort file content lines alphabetically (lexicographic order)."""
        # Preserve a trailing newline if it exists
        had_trailing_newline = content.endswith("\n")
        lines = content.splitlines()
        lines.sort()  # default lexicographic sort, case-sensitive
        out = "\n".join(lines)
        if had_trailing_newline:
            out += "\n"
        return out

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ContentOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.content_config_value import ContentConfigValue
        from wexample_helpers.const.types import StringKeysDict

        return Union[str, dict, StringKeysDict, ContentConfigValue]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.text_config_option import TextConfigOption
        from wexample_filestate.config_option.sort_lines_config_option import SortLinesConfigOption
        from wexample_filestate.config_option.unique_lines_config_option import UniqueLinesConfigOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                TextConfigOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.text_config_option import TextConfigOption
        from wexample_filestate.config_option.sort_lines_config_option import SortLinesConfigOption
        from wexample_filestate.config_option.unique_lines_config_option import UniqueLinesConfigOption

        return [
            TextConfigOption,
            SortLinesConfigOption,
            UniqueLinesConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create FileWriteOperation if content processing is needed."""
        from wexample_filestate.config_option.text_config_option import TextConfigOption
        from wexample_filestate.config_option.sort_lines_config_option import SortLinesConfigOption
        from wexample_filestate.config_option.unique_lines_config_option import UniqueLinesConfigOption
        
        # Get the text content
        text_option = self.get_option_value(TextConfigOption, default=None)
        if not text_option or text_option.is_none():
            return None

        target_content = text_option.get_str()
        if target_content is None:
            return None

        # Apply any class-level content transformations
        class_level_content = target.preview_write(content=target_content)
        if target_content != class_level_content:
            target_content = class_level_content

        # Apply sort_lines if enabled
        sort_lines_option = self.get_option_value(SortLinesConfigOption, default=False)
        if sort_lines_option.is_true():
            target_content = self._sort_lines_content(target_content)

        # Apply unique_lines if enabled
        unique_lines_option = self.get_option_value(UniqueLinesConfigOption, default=False)
        if unique_lines_option.is_true():
            target_content = self._unique_lines_content(target_content)

        # Get current content
        current_content = self._read_current_content(target) or ""

        # If content is different, create operation
        if target_content != current_content:
            return self._create_file_write_operation(target=target, content=target_content)

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

    def _unique_lines_content(self, content: str) -> str:
        """Ensure each line of the file content is unique (remove duplicates preserving order)."""
        # Preserve a trailing newline if it exists
        had_trailing_newline = content.endswith("\n")
        lines = content.splitlines()
        seen: set[str] = set()
        unique_lines: list[str] = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        out = "\n".join(unique_lines)
        if had_trailing_newline:
            out += "\n"
        return out

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()

    def _create_file_write_operation(self, **kwargs):
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        return FileWriteOperation(**kwargs)

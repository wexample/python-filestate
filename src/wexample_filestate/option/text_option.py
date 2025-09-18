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
class TextOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.text_config_value import TextConfigValue
        from wexample_helpers.const.types import StringKeysDict

        # Accept both list form ["trim", "end_new_line"] and dict form {"trim": true, "end_new_line": true}
        return Union[list[str], dict, StringKeysDict, TextConfigValue]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.trim_config_option import TrimConfigOption
        from wexample_filestate.config_option.end_new_line_config_option import EndNewLineConfigOption
        
        # Convert list form to dict form for consistency
        if isinstance(raw_value, list):
            raw_value = {
                TrimConfigOption.get_name(): "trim" in raw_value,
                EndNewLineConfigOption.get_name(): "ensure_newline" in raw_value or "end_new_line" in raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.trim_config_option import TrimConfigOption
        from wexample_filestate.config_option.end_new_line_config_option import EndNewLineConfigOption

        return [
            TrimConfigOption,
            EndNewLineConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create FileWriteOperation if text processing is needed."""
        from wexample_filestate.config_option.trim_config_option import TrimConfigOption
        from wexample_filestate.config_option.end_new_line_config_option import EndNewLineConfigOption
        
        # Get current content
        current_content = self._read_current_content(target)
        if current_content is None:
            return None  # No content to process

        updated_content = current_content
        
        # Apply trim if enabled
        trim_option = self.get_option_value(TrimConfigOption, default=False)
        if trim_option.is_true():
            updated_content = updated_content.strip()

        # Apply end_new_line if enabled
        end_new_line_option = self.get_option_value(EndNewLineConfigOption, default=False)
        if end_new_line_option.is_true():
            if not updated_content.endswith('\n'):
                updated_content += '\n'

        # If content changed, create operation
        if updated_content != current_content:
            return self._create_file_write_operation(target=target, content=updated_content)

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read() or ""

    def _create_file_write_operation(self, **kwargs):
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        return FileWriteOperation(**kwargs)

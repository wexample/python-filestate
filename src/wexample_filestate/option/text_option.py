from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.classes.abstract_method import abstract_method
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
        from wexample_filestate.config_option.end_new_line_config_option import (
            EndNewLineConfigOption,
        )

        # Convert list form to dict form for consistency
        if isinstance(raw_value, list):
            raw_value = {
                TrimConfigOption.get_name(): "trim" in raw_value,
                EndNewLineConfigOption.get_name(): "ensure_newline" in raw_value
                or "end_new_line" in raw_value,
            }

        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.trim_config_option import TrimConfigOption
        from wexample_filestate.config_option.end_new_line_config_option import (
            EndNewLineConfigOption,
        )

        return [
            TrimConfigOption,
            EndNewLineConfigOption,
        ]

    @abstract_method
    def get_description(self) -> str:
        return "Apply rules to text content"

    def create_required_operation(
        self, target: TargetFileOrDirectoryType
    ) -> AbstractOperation | None:
        """Create FileWriteOperation if text processing is needed."""
        from wexample_filestate.config_option.trim_config_option import TrimConfigOption
        from wexample_filestate.config_option.end_new_line_config_option import (
            EndNewLineConfigOption,
        )
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        # Get current content
        current_content = self._read_current_content(target)
        if current_content is None:
            return None  # No content to process

        # Check trim first
        trim_option = self.get_option(TrimConfigOption)
        if trim_option:
            if trim_option.get_value().is_true():
                updated_content = current_content.strip()
                if updated_content != current_content:
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=updated_content,
                        description=trim_option.get_description(),
                    )

        # Check end_new_line second
        end_new_line_option = self.get_option(EndNewLineConfigOption)
        if end_new_line_option:
            if end_new_line_option.get_value().is_true():
                if not current_content.endswith("\n"):
                    updated_content = current_content + "\n"
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=updated_content,
                        description=end_new_line_option.get_description(),
                    )

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read() or ""

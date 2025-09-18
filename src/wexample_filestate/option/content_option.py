from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ContentOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_config.config_value.config_value import ConfigValue

        return Union[str, ConfigValue]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create FileWriteOperation if content differs from current file content."""

        # Get the configured content
        content_value = self.get_value()
        if not content_value or content_value.is_none():
            return None


        # Calculate the target content
        target_content = None
        if content_value.is_str():
            target_content = content_value.get_str()
        # elif isinstance(content_value, ContentConfigValue):
        #     built_content = content_value.build_content()
        #     if built_content is not None:
        #         target_content = built_content

        if target_content is None:
            return None

        # Apply any class-level content transformations
        class_level_content = target.preview_write(content=target_content)
        if target_content != class_level_content:
            target_content = class_level_content

        # Get current content
        current_content = self._read_current_content(target) or ""

        # If content is different, create operation
        if target_content != current_content:
            return self._create_file_write_operation(target=target, content=target_content)

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()

    def _create_file_write_operation(self, target: TargetFileOrDirectoryType, content: str) -> None:
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        return FileWriteOperation(
            target=target,
            content=content
        )

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class ContentOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_config.config_value.config_value import ConfigValue

        return Union[str, ConfigValue]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType
    ) -> AbstractOperation | None:
        """Create FileWriteOperation if content is different."""
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        if not self.get_value().is_none():
            target_content = self.get_value().get_str()
            if target_content is not None:
                # Apply any class-level content transformations
                target_content = target.preview_write(content=target_content)

                # Get current content
                current_content = self._read_current_content(target) or ""

                # If content is different, create operation
                if target_content != current_content:
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=target_content,
                        description=self.get_description(),
                    )

        return None

    def get_description(self) -> str:
        return "Set file content to the specified value"

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()

from __future__ import annotations

from typing import TYPE_CHECKING, Any

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
        return str

    def get_description(self) -> str:
        return "Set file content to the specified value"

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create FileWriteOperation if content is different."""
        from wexample_filestate.operation.file_write_operation import FileWriteOperation

        print(f"DEBUG ContentOption: Checking content for {target.get_path()}")
        print(f"DEBUG ContentOption: Value is_none: {self.get_value().is_none()}")
        
        if not self.get_value().is_none():
            target_content = self.get_value().get_str()
            print(f"DEBUG ContentOption: Target content: {repr(target_content)}")
            
            if target_content is not None:
                # Apply any class-level content transformations
                target_content = target.preview_write(content=target_content)
                print(f"DEBUG ContentOption: After preview_write: {repr(target_content)}")
                
                # Get current content
                current_content = self._read_current_content(target) or ""
                print(f"DEBUG ContentOption: Current content: {repr(current_content)}")
                
                # If content is different, create operation
                if target_content != current_content:
                    print(f"DEBUG ContentOption: Content differs, creating FileWriteOperation")
                    return FileWriteOperation(
                        option=self,
                        target=target,
                        content=target_content,
                        description=self.get_description(),
                    )
                else:
                    print(f"DEBUG ContentOption: Content is same, no operation needed")
            else:
                print(f"DEBUG ContentOption: Target content is None")
        else:
            print(f"DEBUG ContentOption: Value is None")

        return None

    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()

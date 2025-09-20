from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class OnBadFormatOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str
    
    def get_description(self) -> str:
        return "Action to take when name format validation fails (delete, rename, ignore, error)"

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, parent_option=None
    ) -> AbstractOperation | None:
        """Create operation based on the action when format validation fails."""
        if not parent_option:
            return None
            
        # Get the current name
        current_name = target.get_name()
        
        # Validate name using parent NameFormatOption
        if parent_option.validate_name(current_name):
            return None  # Name is valid, no action needed
            
        # Name is invalid, take action based on configuration
        action = self.get_value().get_str()
        
        if action == "delete":
            from wexample_filestate.operation.file_remove_operation import FileRemoveOperation
            return FileRemoveOperation(
                option=self,
                target=target,
                description=f"Delete file with invalid name format: {current_name}"
            )
        elif action == "rename":
            # TODO: Implement rename logic based on format rules
            # For now, just log that rename would happen
            return None
        elif action == "error":
            from wexample_filestate.exception.name_format_exception import NameFormatException
            raise NameFormatException(f"File name '{current_name}' does not match required format")
        # "ignore" action returns None (no operation)
        
        return None

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class OptionMixin(ItemTreeConfigOptionMixin):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Option"

    @abstract_method
    def is_satisfied(self, target: TargetFileOrDirectoryType) -> bool:
        """Check if the current state satisfies this option's requirements.
        
        Returns:
            True if the option requirements are met, False otherwise
        """
        pass

    @abstract_method
    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create and configure an operation instance when this option is not satisfied.
        
        Returns:
            None if no operation is needed (option is satisfied)
            AbstractOperation instance configured with necessary data if action is required
            
        The option is responsible for:
        - Instantiating the appropriate operation class
        - Configuring the operation with necessary data
        - Passing any computed values (e.g., new content for FileWriteOperation)
        """
        pass

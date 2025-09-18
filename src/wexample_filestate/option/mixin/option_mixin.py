from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_file.enum.local_path_type import LocalPathType
from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class OptionMixin(ItemTreeConfigOptionMixin):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Option"

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create and configure an operation instance if this option requires action.
        
        Returns:
            None if no operation is needed (option is satisfied or not applicable)
            AbstractOperation instance configured with necessary data if action is required
            
        The option is responsible for:
        - Determining if action is needed
        - Instantiating the appropriate operation class
        - Configuring the operation with necessary data
        - Passing any computed values (e.g., new content for FileWriteOperation)
        """
        return None

    def get_supported_item_types(self) -> list[LocalPathType]:
        return [
            LocalPathType.FILE,
            LocalPathType.DIRECTORY,
        ]

    def applicable_on_file(self) -> bool:
        return True

    def applicable_on_directory(self) -> bool:
        return True

    def applicable_on_missing(self) -> bool:
        return True

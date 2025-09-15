from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class ModeOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.const.files import FileSystemPermission

        return Union[str, int, FileSystemPermission]

    def get_int(self) -> int:
        from wexample_helpers.helpers.file import file_mode_octal_to_num

        return file_mode_octal_to_num(self.get_octal())

    def get_octal(self) -> str:
        value = self.get_value()

        if value.is_str():
            return value.get_str()
        elif value.is_int():
            return value.to_str()
        elif value.is_dict():
            value_dict = value.get_dict()
            if value_dict.get("mode"):
                return str(value["mode"])

        raise ValueError(f"Unexpected value in get_octal: {value}")

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create ItemChangeModeOperation if current mode differs from target mode."""
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
        from wexample_helpers.helpers.file import (
            file_path_get_mode_num,
            file_validate_mode_octal_or_fail,
        )

        # Check if target has a source (file/directory exists)
        if not target.source:
            return None

        try:
            # Validate the configured mode
            file_validate_mode_octal_or_fail(self.get_octal())
            
            # Get current mode and compare with target mode
            current_mode = file_path_get_mode_num(target.get_source().get_path())
            target_mode = self.get_int()
            
            # If modes are different, create the operation
            if current_mode != target_mode:
                return self._create_mode_operation(target=target, target_mode=target_mode)
                
        except Exception:
            # If validation fails or any error occurs, don't create operation
            return None
            
        return None

    def _create_mode_operation(self, **kwargs):
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
        return ItemChangeModeOperation(**kwargs)
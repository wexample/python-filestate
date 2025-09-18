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
class ModeOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str, int, dict]

    def get_int(self) -> int:
        from wexample_helpers.helpers.file import file_mode_octal_to_num

        return file_mode_octal_to_num(self.get_octal())

    def get_octal(self) -> str:
        from wexample_filestate.config_option.permissions_config_option import PermissionsConfigOption
        return self.get_value().get_dict().get(PermissionsConfigOption.get_name())

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.permissions_config_option import PermissionsConfigOption
        # Always work with a dict.
        if not isinstance(raw_value, dict):
            raw_value = {
                PermissionsConfigOption.get_name(): str(raw_value)
            }

        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.recursive_config_option import RecursiveConfigOption
        from wexample_filestate.config_option.permissions_config_option import PermissionsConfigOption

        return [
            PermissionsConfigOption,
            RecursiveConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create ItemChangeModeOperation if current mode differs from target mode."""
        from wexample_helpers.helpers.file import (
            file_path_get_mode_num,
            file_validate_mode_octal_or_fail,
        )

        # Check if target has a source (file/directory exists)
        if not target.source:
            return None

        # Validate the configured mode
        file_validate_mode_octal_or_fail(self.get_octal())

        # Get current mode and compare with target mode
        current_mode = file_path_get_mode_num(target.get_source().get_path())
        target_mode = self.get_int()

        # If modes are different, create the operation
        if current_mode != target_mode:
            return self._create_mode_operation(target=target, target_mode=target_mode)

        return None

    def _create_mode_operation(self, **kwargs):
        from wexample_filestate.config_option.recursive_config_option import RecursiveConfigOption
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation

        # Check if recursive flag should be set from dict format
        if self.get_option_value(RecursiveConfigOption, default=False).is_true():
            kwargs[RecursiveConfigOption.get_name()] = True

        return ItemChangeModeOperation(**kwargs)

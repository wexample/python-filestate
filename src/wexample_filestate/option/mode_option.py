from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import (
    AbstractNestedConfigOption,
)
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class ModeOption(OptionMixin, AbstractNestedConfigOption):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        return [Scope.PERMISSIONS]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.mode_config_value import ModeConfigValue

        return Union[str, int, dict, ModeConfigValue]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create ItemChangeModeOperation if current mode differs from target mode."""
        from wexample_helpers.helpers.file import (
            file_mode_apply_notation,
            file_mode_is_notation,
            file_mode_num_to_octal,
            file_mode_octal_to_num,
            file_path_get_mode_num,
            file_validate_mode_octal_or_fail,
        )

        from wexample_filestate.operation.file_change_mode_operation import (
            FileChangeModeOperation,
        )
        from wexample_filestate.option.mode.recursive_option import RecursiveOption

        # Check if target has a source (file/directory exists)
        if not target.source:
            return None

        current_mode = file_path_get_mode_num(target.get_source().get_path())
        permissions = self.get_octal()

        if file_mode_is_notation(permissions):
            target_mode = file_mode_apply_notation(current_mode, permissions)
        else:
            file_validate_mode_octal_or_fail(permissions)
            target_mode = file_mode_octal_to_num(permissions)

        if current_mode != target_mode:
            return FileChangeModeOperation(
                option=self,
                target=target,
                target_mode=target_mode,
                recursive=self.get_option_value(
                    RecursiveOption, default=False
                ).is_true(),
                description=f"Update file permissions from {file_mode_num_to_octal(current_mode)} to {file_mode_num_to_octal(target_mode)}",
            )

        return None

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption

        return [
            PermissionsOption,
            RecursiveOption,
        ]

    def get_octal(self) -> str:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption

        return self.get_value().get_dict().get(PermissionsOption.get_name())

    def prepare_value(self, raw_value: Any) -> Any:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption

        # Always work with a dict.
        if isinstance(raw_value, str) or isinstance(raw_value, int):
            raw_value = {PermissionsOption.get_name(): str(raw_value)}

        return super().prepare_value(raw_value=raw_value)

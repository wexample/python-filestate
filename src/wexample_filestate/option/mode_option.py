from __future__ import annotations

import os
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
        return [Scope.PERMISSIONS, Scope.OWNERSHIP]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.mode_config_value import ModeConfigValue

        return Union[str, int, dict, ModeConfigValue]

    def create_required_operation(
        self, target: TargetFileOrDirectoryType, scopes: set[Scope]
    ) -> AbstractOperation | None:
        """Create an operation if current permissions or owner differ from target."""
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
        from wexample_filestate.operation.file_chown_operation import FileChownOperation
        from wexample_filestate.option.mode.owner_option import OwnerOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption

        if not target.source:
            return None

        source_path = target.get_source().get_path()
        recursive = self.get_option_value(RecursiveOption, default=False).is_true()

        # --- Permissions ---
        needs_chmod = False
        target_mode = None
        current_mode = None
        permissions = self.get_octal()

        if permissions is not None:
            current_mode = file_path_get_mode_num(source_path)
            if file_mode_is_notation(permissions):
                target_mode = file_mode_apply_notation(current_mode, permissions)
            else:
                file_validate_mode_octal_or_fail(permissions)
                target_mode = file_mode_octal_to_num(permissions)
            needs_chmod = current_mode != target_mode

        # --- Owner ---
        needs_chown = False
        target_uid: int | None = None
        target_gid: int | None = None
        owner_raw = self.get_owner_raw()

        if owner_raw is not None:
            target_uid, target_gid = OwnerOption.resolve(owner_raw)
            stat = os.stat(source_path)
            needs_chown = (
                target_uid is not None and stat.st_uid != target_uid
            ) or (
                target_gid is not None and stat.st_gid != target_gid
            )

        # --- Build operation ---
        if needs_chmod:
            description = f"Update permissions from {file_mode_num_to_octal(current_mode)} to {file_mode_num_to_octal(target_mode)}"
            if needs_chown:
                description += f" and owner to {target_uid}:{target_gid}"
            return FileChangeModeOperation(
                option=self,
                target=target,
                target_mode=target_mode,
                target_uid=target_uid if needs_chown else None,
                target_gid=target_gid if needs_chown else None,
                recursive=recursive,
                description=description,
            )

        if needs_chown:
            return FileChownOperation(
                option=self,
                target=target,
                target_uid=target_uid,
                target_gid=target_gid,
                recursive=recursive,
                description=f"Update owner to {target_uid}:{target_gid}",
            )

        return None

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.mode.owner_option import OwnerOption
        from wexample_filestate.option.mode.permissions_option import PermissionsOption
        from wexample_filestate.option.mode.recursive_option import RecursiveOption

        return [
            PermissionsOption,
            RecursiveOption,
            OwnerOption,
        ]

    def get_octal(self) -> str | None:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption

        return self.get_value().get_dict().get(PermissionsOption.get_name())

    def get_owner_raw(self) -> str | None:
        from wexample_filestate.option.mode.owner_option import OwnerOption

        return self.get_value().get_dict().get(OwnerOption.get_name())

    def prepare_value(self, raw_value: Any) -> Any:
        from wexample_filestate.option.mode.permissions_option import PermissionsOption

        # Always work with a dict.
        if isinstance(raw_value, str) or isinstance(raw_value, int):
            raw_value = {PermissionsOption.get_name(): str(raw_value)}

        return super().prepare_value(raw_value=raw_value)

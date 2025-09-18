from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.permissions_config_option import PermissionsConfigOption
from wexample_filestate.config_option.recursive_config_option import RecursiveConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class ModeConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    permissions: str | int = public_field(
        description="The expected file permission",
    )
    recursive: bool | None = public_field(
        default=None,
        description="Apply to sub items if origin is a directory",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            PermissionsConfigOption.get_name(): self.permissions,
            RecursiveConfigOption.get_name(): self.recursive,
        }

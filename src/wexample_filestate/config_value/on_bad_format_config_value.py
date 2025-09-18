from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.action_config_option import ActionConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class OnBadFormatConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    action: str | None = public_field(
        default=None,
        description="Action to take when name format is invalid: delete, rename, ignore, error",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            ActionConfigOption.get_name(): self.action,
        }

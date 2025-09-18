from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.value_config_option import ValueConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    value: str = public_field(
        description="The name value",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            ValueConfigOption.get_name(): self.value,
        }

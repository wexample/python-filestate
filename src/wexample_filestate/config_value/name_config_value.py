from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.value_config_option import ValueConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_filestate.option.name_format.case_format_option import CaseFormatOption
from wexample_filestate.option.name_format.prefix_option import PrefixOption
from wexample_filestate.option.name_format.regex_option import RegexOption
from wexample_filestate.option.name_format.suffix_option import SuffixOption


@base_class
class NameConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    value: str = public_field(
        description="The name value",
    )
    case_format: str | None = public_field(
        default=None,
        description="Case format: uppercase, lowercase, camelCase, snake_case, kebab-case",
    )
    regex: str | None = public_field(
        default=None,
        description="Regular expression pattern the name must match",
    )
    prefix: str | None = public_field(
        default=None,
        description="Required prefix for the name",
    )
    suffix: str | None = public_field(
        default=None,
        description="Required suffix for the name",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            ValueConfigOption.get_name(): self.value,
            CaseFormatOption.get_name(): self.case_format,
            RegexOption.get_name(): self.regex,
            PrefixOption.get_name(): self.prefix,
            SuffixOption.get_name(): self.suffix,
        }

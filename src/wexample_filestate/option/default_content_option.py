from __future__ import annotations

from collections.abc import Callable
from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.config_value import ConfigValue
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin


@base_class
class DefaultContentOption(OptionMixin, AbstractConfigOption):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        return [Scope.CONTENT]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str, ConfigValue, Callable]

    def get_value(self) -> ConfigValue:
        """Resolve callable values just like ContentOption, so callers can pass
        either a literal string/ConfigValue or a lambda(target) → str."""
        value = super().get_value()

        if isinstance(value, str):
            return ConfigValue(raw=value)
        if value.is_callable():
            return ConfigValue(raw=str((value.get_callable())(self)))

        return value

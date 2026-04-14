from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
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
        from wexample_config.config_value.config_value import ConfigValue

        return Union[str, ConfigValue]

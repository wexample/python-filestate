from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class YamlFilterOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict

        # Accept both list form ["sort_recursive"] and dict form if extended later
        return Union[list[str], StringKeysDict]

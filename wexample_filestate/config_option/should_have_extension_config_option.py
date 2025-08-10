from typing import Any, Union

from wexample_helpers.const.types import StringsList
from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ShouldHaveExtensionConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str | StringsList]

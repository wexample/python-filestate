from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.config_option.mixin.renderable_config_option_mixin import (
    RenderableConfigOptionMixin,
)


class DefaultContentConfigOption(RenderableConfigOptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

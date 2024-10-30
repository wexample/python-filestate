from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ShouldExistConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Any:
        return bool
from typing import Any, List

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class NamePatternConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str | List[str]

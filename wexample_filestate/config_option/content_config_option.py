from typing import Union, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ContentConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str]

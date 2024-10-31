from typing import Any

from wexample_config.config_option.abstract_config_option import \
    AbstractConfigOption


class DefaultContentConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

    def render_content(self) -> str:
        return self.get_value().get_str()

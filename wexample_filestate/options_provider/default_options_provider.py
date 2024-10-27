from typing import List, TYPE_CHECKING, Type
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_config.option.abstract_option import AbstractOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractOption"]]:
        from wexample_config.option.name_option import NameOption

        return [
            NameOption,
        ]

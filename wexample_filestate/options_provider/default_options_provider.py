from typing import List, TYPE_CHECKING, Type

from wexample_config.option.children_option import ChildrenOption
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.option.mode_option import ModeOption
from wexample_filestate.option.type_option import TypeOption

if TYPE_CHECKING:
    from wexample_config.option.abstract_option import AbstractOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractOption"]]:
        from wexample_config.option.name_option import NameOption

        return [
            ChildrenOption,
            ModeOption,
            NameOption,
            TypeOption,
        ]

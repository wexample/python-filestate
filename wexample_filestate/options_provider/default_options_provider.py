from typing import List, TYPE_CHECKING, Type

from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_filestate.options.abstract_option import AbstractOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    def get_options(self) -> List[Type["AbstractOption"]]:
        from wexample_filestate.options.name_option import NameOption
        from wexample_filestate.options.mode_option import ModeOption
        from wexample_filestate.options.should_exist_option import ShouldExistOption

        return [
            ModeOption,
            NameOption,
            ShouldExistOption,
        ]

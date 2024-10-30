from pathlib import Path
from typing import TYPE_CHECKING, List, Optional, Type

from wexample_config.config_option.abstract_nested_config_option import \
    AbstractNestedConfigOption
from wexample_config.const.types import DictConfig
from wexample_helpers.const.types import FileStringOrPath

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import \
        AbstractOptionsProvider


class StateItemTargetMixin(AbstractNestedConfigOption):
    base_path: FileStringOrPath
    path: Optional[Path] = None

    def __init__(self, config: DictConfig, **data):
        AbstractNestedConfigOption.__init__(self, value=config, **data)

        self.path = Path(f"{self.base_path}{config['name']}")

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        providers = super().get_options_providers()
        if len(providers) > 0:
            return providers

        from wexample_filestate.options_provider.default_options_provider import \
            DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]

    def get_item_name(self) -> Optional[str]:
        from wexample_config.config_option.name_config_option import \
            NameConfigOption

        option = self.get_option(NameConfigOption)

        return option.get_value().get_str() if option else None

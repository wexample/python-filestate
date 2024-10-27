from typing import Optional, List, Type, TYPE_CHECKING, cast
from pydantic import BaseModel
from wexample_config.const.types import StateItemConfig

if TYPE_CHECKING:
    from wexample_config.option.abstract_option import AbstractOption
    from wexample_config.src.config_manager import ConfigManager
    from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider


class StateItemTargetMixin(BaseModel):
    config_manager: Optional["ConfigManager"] = None

    def __init__(self, config: Optional[StateItemConfig] = None, **data):
        super().__init__(**data)

        config = self.build_config(config)

        if config:
            self.configure(config)

    def build_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        return config or {}

    def get_options_providers(self) -> List[Type["AbstractOptionsProvider"]]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]

    def get_all_options(self) -> List[Type["AbstractOption"]]:
        providers = self.get_options_providers()
        options = []

        for provider in providers:
            options.extend(cast("AbstractOptionsProvider", provider).get_options())

        return options

    def configure(self, config: Optional[StateItemConfig]) -> None:
        from wexample_config.src.config_manager import ConfigManager

        self.config_manager = ConfigManager(config=config)

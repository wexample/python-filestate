from typing import Optional

from pydantic import BaseModel

from wexample_config.const.types import StateItemConfig
from wexample_config.src.config_manager import ConfigManager


class StateItemTargetMixin(BaseModel):
    config_manager: Optional[ConfigManager] = None

    def __init__(self, config: Optional[StateItemConfig] = None, **data):
        super().__init__(**data)

        config = self.build_config(config)

        if config:
            self.configure(config)

    def build_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        return config or {}

    def configure(self, config: Optional[StateItemConfig]) -> None:
        self.config_manager = ConfigManager(config=config)

from typing import Optional

from pydantic import BaseModel

from wexample_config.const.types import StateItemConfig


class StateItemTargetMixin(BaseModel):
    config: Optional[StateItemConfig] = None

    def __init__(self, config: Optional[StateItemConfig] = None, **data):
        super().__init__(**data)

        config = self.build_config(config)

        if config:
            self.configure(config)

    def build_config(self, config: Optional[StateItemConfig] = None) -> StateItemConfig:
        return config or {}

    def configure(self, config: Optional[StateItemConfig]) -> None:
        pass

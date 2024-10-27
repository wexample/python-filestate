from typing import Optional

from pydantic import BaseModel

from wexample_config.const.types import StateItemConfig


class StateItemTargetMixin(BaseModel):
    config: Optional[StateItemConfig] = None

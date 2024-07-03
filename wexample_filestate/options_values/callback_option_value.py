from typing import Callable, Any, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
    from wexample_filestate.const.types import StateItemConfig


class CallbackOptionValue(BaseModel):
    callback: Callable[["StateItemTargetMixin", "StateItemConfig"], Any]

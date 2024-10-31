from typing import Callable, Any, TYPE_CHECKING


from wexample_filestate.config_value.item_config_value import ItemConfigValue

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory

class CallbackOptionValue(ItemConfigValue):
    callback: Callable[["TargetFileOrDirectory", "DictConfig"], Any]

    def __init__(self, callback: Callable[["TargetFileOrDirectory", "DictConfig"], Any], **data):
        super().__init__(raw=callback, callback=callback, **data)

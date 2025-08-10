from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.item.item_target_directory import ItemTargetDirectory


class ShortcutConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

    def __init__(self, **data) -> None:
        super().__init__(**data)

        # The parent should always be a path item.
        assert isinstance(self.parent, AbstractItemTarget)

        # The root should always be a directory.
        root = self.parent.get_root()
        assert isinstance(root, ItemTargetDirectory)

        root.set_shortcut(self.get_value().get_str(), self.parent)

from __future__ import annotations

from typing import Any

from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class ShortcutOption(OptionMixin, AbstractConfigOption):
    def __attrs_post_init__(self) -> None:
        from wexample_filestate.item.abstract_item_target import AbstractItemTarget

        super().__attrs_post_init__()

        # The parent should always be a path item.
        assert isinstance(self.parent, AbstractItemTarget)

        # If no parent, root might be a file as it returns itself.
        root = self.parent.get_root()
        assert isinstance(root, AbstractItemTarget)

        # Register shortcuts only in root directories.
        if root != self.parent and root.is_directory():
            root.set_shortcut(self.get_value().get_str(), self.parent)

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return str

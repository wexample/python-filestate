from __future__ import annotations

from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin


class OptionMixin(ItemTreeConfigOptionMixin):
    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "Option"

    def get_required_operations(self, target) -> list:
        """Return operation instances that should be executed when this option is not satisfied.
        """
        return []

    def is_satisfied(self, target) -> bool:
        """Check if the current state satisfies this option's requirements.
        """
        return True

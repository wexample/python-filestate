from __future__ import annotations

from typing import Any

from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class ShouldExistOption(OptionMixin, AbstractConfigOption):
    value: Any = public_field(
        default=None,
        description="Boolean flag indicating whether the option must exist",
    )

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        # Replace None with True (preserves existing values)
        if self.value is None:
            self.value = True

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

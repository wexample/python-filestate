from __future__ import annotations

from typing import Any, Union

from wexample_filestate.option.mode_option import ModeOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class ModeRecursiveOption(ModeOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[str, int, bool]

    def _create_mode_operation(self, **kwargs):
        kwargs['recursive'] = True
        return super()._create_mode_operation(**kwargs)

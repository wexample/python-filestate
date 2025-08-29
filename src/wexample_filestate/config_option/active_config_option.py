from __future__ import annotations

from collections.abc import Callable
from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ActiveConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[bool, Callable[..., Any]]

    @staticmethod
    def is_active(value: Union[bool, Callable[..., Any]]) -> bool:
        if callable(value):
            return bool(value())

        return value is True

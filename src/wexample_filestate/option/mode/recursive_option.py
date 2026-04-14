from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class

from wexample_filestate.enum.scopes import Scope
from wexample_filestate.option.mixin.option_mixin import OptionMixin


@base_class
class RecursiveOption(OptionMixin, AbstractConfigOption):
    @classmethod
    def get_scopes(cls) -> list[Scope]:
        return [Scope.PERMISSIONS]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool

    def get_description(self) -> str:
        return "Apply mode changes recursively to subdirectories and files"

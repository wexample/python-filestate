from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import attrs
from wexample_helpers.classes.base_class import BaseClass
from wexample_filestate.const.state_items import TargetFileOrDirectory
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.enum.scopes import Scope


@attrs.define(kw_only=True)
class AbstractOperation(HasSnakeShortClassNameClassMixin, BaseClass):
    applied: bool = attrs.field(default=False)
    target: TargetFileOrDirectory
    _tty_width: int = attrs.field(default=80, init=False)

    @classmethod
    @abstractmethod
    def get_scope(cls) -> Scope:
        pass

    def applicable(self) -> bool:
        for option in self.target.options.values():
            if self.applicable_for_option(option=option) is True:
                return True

        return False

    @abstractmethod
    def applicable_for_option(self, option: AbstractConfigOption) -> bool:
        pass

    @abstractmethod
    def apply(self) -> None:
        pass

    def dependencies(self) -> list[type[AbstractOperation]]:
        return []

    @abstractmethod
    def describe_after(self) -> str:
        pass

    @abstractmethod
    def describe_before(self) -> str:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    def _build_str_value(self, value: Any) -> str:
        built = self._build_value(value)
        if not isinstance(built, str):
            raise TypeError(
                f"Expected string value, got {type(built).__name__}: {built}"
            )
        return built

    def _build_value(self, value: Any) -> Any:
        """
        First version, might be tested / replaced / abstracted to every callable option.
        Always return the built (resolved) value, never a callable:
        - ConfigValue callable -> execute with self.target and return result
        - ConfigValue str -> return str
        - ConfigValue other -> return raw (then resolved below if callable)
        - Plain callable -> execute with self.target and return result
        - Plain str -> return as-is
        - Other -> return as-is
        Legacy dict {'pattern': ...} is intentionally unsupported.
        """
        from wexample_config.config_value.config_value import ConfigValue

        # ConfigValue case
        if isinstance(value, ConfigValue):
            if value.is_callable():
                fn = value.get_callable()
                value = fn(self.target)
            elif value.is_str():
                value = value.get_str()
            else:
                value = value.raw

        # Resolve plain callable
        if callable(value):
            value = value(self.target)

        return value

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.const.state_items import TargetFileOrDirectory
    from wexample_filestate.enum.scopes import Scope


@base_class
class AbstractOperation(HasSnakeShortClassNameClassMixin, BaseClass):
    applied: bool = public_field(
        description="Flag indicating whether the operation has already been applied",
        default=False,
    )
    target: TargetFileOrDirectory = public_field(
        description="The target file or directory on which this operation is executed",
    )
    _tty_width: int = private_field(
        description="The terminal width in characters used for display formatting",
        default=80,
    )

    @classmethod
    @abstract_method
    def get_scope(cls) -> Scope:
        pass


    @abstract_method
    def apply(self) -> None:
        pass


    @abstract_method
    def describe_after(self) -> str:
        pass

    @abstract_method
    def describe_before(self) -> str:
        pass

    @abstract_method
    def description(self) -> str:
        pass

    @abstract_method
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

    @classmethod
    def matches_filter(cls, filter_name: str) -> bool:
        import fnmatch
        return fnmatch.fnmatch(cls.get_name(), filter_name)

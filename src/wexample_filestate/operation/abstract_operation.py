from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

from pydantic import BaseModel

from wexample_filestate.const.state_items import TargetFileOrDirectory
from wexample_filestate.enum.scopes import Scope
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_value.config_value import ConfigValue
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )


class AbstractOperation(HasSnakeShortClassNameClassMixin, BaseModel):
    applied: bool = False
    target: TargetFileOrDirectory
    _tty_width: int = 80

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

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def describe_before(self) -> str:
        pass

    @abstractmethod
    def describe_after(self) -> str:
        pass

    def dependencies(self) -> list[type[AbstractOperation]]:
        return []

    def _build_value(self, value: ConfigValue) -> Any:
        if value.is_str():
            return value.get_str()
        elif value.is_dict() and "pattern" in value.get_dict():
            path = self.target.get_path()
            value_dict = value.get_dict()

            return value_dict["pattern"].format(
                **{"name": path.name, "path": str(path)}
            )

        return value.get_str()
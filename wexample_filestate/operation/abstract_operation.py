from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Type

from pydantic import BaseModel
from wexample_filestate.enum.scopes import Scope
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import \
    HasSnakeShortClassNameClassMixin

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import \
        AbstractConfigOption
    from wexample_filestate.const.state_items import TargetFileOrDirectory


class AbstractOperation(HasSnakeShortClassNameClassMixin, BaseModel):
    applied: bool = False
    target: "TargetFileOrDirectory"
    _tty_width: int = 80

    @classmethod
    @abstractmethod
    def get_scope(cls) -> Scope:
        pass

    @classmethod
    def applicable(cls, target: "TargetFileOrDirectory") -> bool:
        for option in target.options.values():
            if cls.applicable_option(target=target, option=option) is True:
                return True

        return False

    @staticmethod
    @abstractmethod
    def applicable_option(
        target: "TargetFileOrDirectory", option: "AbstractConfigOption"
    ) -> bool:
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

    def dependencies(self) -> List[Type["AbstractOperation"]]:
        return []

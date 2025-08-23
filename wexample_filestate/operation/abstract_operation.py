from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

from pydantic import BaseModel
from wexample_filestate.const.state_items import TargetFileOrDirectory
from wexample_filestate.enum.scopes import Scope
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)

if TYPE_CHECKING:
    from wexample_config.config_option.abstract_config_option import (
        AbstractConfigOption,
    )
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class AbstractOperation(HasSnakeShortClassNameClassMixin, BaseModel):
    applied: bool = False
    target: TargetFileOrDirectory
    _tty_width: int = 80

    @classmethod
    @abstractmethod
    def get_scope(cls) -> Scope:
        pass

    def applicable(self, target: TargetFileOrDirectory) -> bool:
        for option in target.options.values():
            if self.applicable_operation(target=target, option=option) is True:
                return True

        return False

    @abstractmethod
    def applicable_operation(
        self, target: TargetFileOrDirectoryType, option: AbstractConfigOption
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

    def dependencies(self) -> list[type[AbstractOperation]]:
        return []

from __future__ import annotations

import os
from abc import abstractmethod, ABC

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class AbstractOperation(BaseModel, ABC):
    target: TargetFileOrDirectory
    _before: int | str | None = None
    _after: int | str | None = None

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @staticmethod
    @abstractmethod
    def applicable(target: TargetFileOrDirectory) -> bool:
        pass

    @abstractmethod
    def apply(self) -> None:
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

    def to_tty(self) -> str:
        return os.linesep.join([
            f'{self.target.get_item_title()}: {self.target.path.resolve()}',
            f'{self.description()}:',
            f'    Before: {self._before}',
            f'    After: {self._after}',
        ])

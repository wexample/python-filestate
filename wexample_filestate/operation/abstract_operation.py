from __future__ import annotations

from abc import abstractmethod

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class AbstractOperation(BaseModel):
    target: TargetFileOrDirectory

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
    def to_tty(self) -> str:
        pass

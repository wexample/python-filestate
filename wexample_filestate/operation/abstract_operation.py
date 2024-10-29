from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_helpers.helpers.array_helper import array_swap
from wexample_prompt.utils.prompt_response import PromptResponse


class AbstractOperation(BaseModel, ABC):
    applied: bool = False
    target: TargetFileOrDirectory
    _tty_width: int = 80

    @staticmethod
    @abstractmethod
    def applicable(target: TargetFileOrDirectory) -> bool:
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

    def dependencies(self) -> List["AbstractOperation"]:
        return []

    def to_prompt_response(self, rollback: bool) -> PromptResponse:
        lines = [
            f'{"TASK" if not rollback else "ROLLBACK"} '.ljust(self._tty_width, '_')
        ]

        before, after = array_swap(
            [
                self.describe_before(),
                self.describe_after(),
            ],
            do_swap=rollback,
        )

        lines.extend(
            [
                f'{self.target.get_item_title()}: {self.target.path.resolve()}',
                f'{self.description()}:',
                f'    Before: {before}',
                f'    After: {after}',
            ]
        )

        return PromptResponse.from_lines(lines)

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
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

    def dependencies(self) -> List["AbstractOperation"]:
        return []

    def to_prompt_response(self, rollback: bool) -> PromptResponse:
        lines = [
            f'{"TASK" if not rollback else "ROLLBACK"} '.ljust(self._tty_width, '_')
        ]

        return PromptResponse.from_lines(lines)

    def get_target_file_path(self) -> str:
        return self.target.path.resolve().as_posix()

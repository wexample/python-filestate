from __future__ import annotations
from abc import ABC, abstractmethod
from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_prompt.utils.prompt_response import PromptResponse


class AbstractOperation(BaseModel, ABC):
    _tty_width: int = 80

    @staticmethod
    @abstractmethod
    def applicable(target: TargetFileOrDirectory) -> bool:
        pass

    def to_prompt_response(self, rollback: bool) -> PromptResponse:
        lines = [
            f'{"TASK" if not rollback else "ROLLBACK"} '.ljust(self._tty_width, '_')
        ]

        return PromptResponse.from_lines(lines)

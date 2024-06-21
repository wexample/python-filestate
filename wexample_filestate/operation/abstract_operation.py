from __future__ import annotations

from abc import abstractmethod, ABC

from pydantic import BaseModel

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_prompt.utils.prompt_response import PromptResponse


class AbstractOperation(BaseModel, ABC):
    target: TargetFileOrDirectory
    _before: int | str | None = None
    _after: int | str | None = None
    _tty_width: int = 80

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

    def to_prompt_response(self) -> PromptResponse:
        return PromptResponse.from_lines([
            f'TASK '.ljust(self._tty_width, '_'),
            f'{self.target.get_item_title()}: {self.target.path.resolve()}',
            f'{self.description()}:',
            f'    Before: {self.describe_before()}',
            f'    After: {self.describe_after()}',
        ])

from __future__ import annotations

from typing import List, TYPE_CHECKING

from pydantic import BaseModel

from wexample_prompt.utils.prompt_response import PromptResponse

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

class AbstractResult(BaseModel):
    state_manager: 'FileStateItemDirectoryTarget'
    _operations: List["AbstractOperation"]
    rollback: bool = False

    def __init__(self, **data):
        super().__init__(**data)
        self._operations = []

    @property
    def operations(self) -> List["AbstractOperation"]:
        return self._operations

    def to_prompt_responses(self) -> List[PromptResponse]:
        output: List[PromptResponse] = []

        for operation in self.operations:
            output.append(operation.to_prompt_response(self.rollback))

        return output

    def print(self) -> None:
        responses = self.to_prompt_responses()

        self.state_manager.io.print_responses(
            responses
        )

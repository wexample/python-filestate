from __future__ import annotations

from typing import List, TYPE_CHECKING

from pydantic import BaseModel

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_prompt.utils.prompt_response import PromptResponse

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractResult(BaseModel):
    state_manager: 'FileStateManager'
    operations: List[AbstractOperation] = []
    rollback: bool = False

    def to_prompt_responses(self) -> List[PromptResponse]:
        output: List[PromptResponse] = []

        for operation in self.operations:
            output.append(operation.to_prompt_response(self.rollback))

        return output

    def print(self) -> List[PromptResponse]:
        responses = self.to_prompt_responses()

        self.state_manager.io.print_responses(
            responses
        )

        return responses

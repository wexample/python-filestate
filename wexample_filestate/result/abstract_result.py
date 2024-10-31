from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import BaseModel
from wexample_prompt.utils.prompt_response import PromptResponse
from wexample_filestate.operation.abstract_operation import \
    AbstractOperation


if TYPE_CHECKING:
    from wexample_filestate.item.file_state_item_directory_target import \
        FileStateItemDirectoryTarget

class AbstractResult(BaseModel):
    state_manager: "FileStateItemDirectoryTarget"
    operations: List[AbstractOperation] = []
    rollback: bool = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return f"{self.__repr__}"

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

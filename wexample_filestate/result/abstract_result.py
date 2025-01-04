from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import BaseModel
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_prompt.responses import BasePromptResponse

if TYPE_CHECKING:
    from wexample_filestate.item.item_target_directory import (
        ItemTargetDirectory,
    )


class AbstractResult(BaseModel):
    state_manager: "ItemTargetDirectory"
    operations: List[AbstractOperation] = []
    rollback: bool = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return f"{self.__repr__}"

    def to_prompt_responses(self) -> List[BasePromptResponse]:
        output: List[BasePromptResponse] = []

        for operation in self.operations:
            output.append(operation.to_prompt_response(self.rollback))

        return output

    def print(self) -> None:
        responses = self.to_prompt_responses()

        self.state_manager.io.print_responses(responses)

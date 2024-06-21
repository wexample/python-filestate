from __future__ import annotations

from typing import List

from pydantic import BaseModel

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_prompt.utils.prompt_response import PromptResponse


class AbstractResult(BaseModel):
    operations: List[AbstractOperation] = []

    def to_prompt_responses(self) -> List[PromptResponse]:
        output: List[PromptResponse] = []

        for operation in self.operations:
            output.append(operation.to_prompt_response())

        return output

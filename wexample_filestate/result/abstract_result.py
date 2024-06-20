from __future__ import annotations

from typing import List

from pydantic import BaseModel

from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractResult(BaseModel):
    operations: List[AbstractOperation] = []

    def to_tty(self) -> List[str]:
        output = []

        for operation in self.operations:
            output.append(operation.to_tty())

        return output

from __future__ import annotations

import os
from typing import List

from pydantic import BaseModel

from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractResult(BaseModel):
    operations: List[AbstractOperation] = []

    def to_tty(self) -> str:
        output = []

        for operation in self.operations:
            output.append(operation.to_tty())

        return os.linesep.join(output)

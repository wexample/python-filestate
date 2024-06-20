from typing import List
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractResult(BaseModel):
    operations: List["AbstractOperation"] = []

    def to_tty(self) -> List[str]:
        output = []

        for operation in self.operations:
            output.append(operation.to_tty())

        return output

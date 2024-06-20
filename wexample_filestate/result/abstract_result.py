from typing import List, Type

from pydantic import BaseModel

from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractResult(BaseModel):
    operations: List[Type[AbstractOperation]] = []

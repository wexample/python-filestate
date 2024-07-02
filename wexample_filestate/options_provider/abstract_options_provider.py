from abc import ABC, abstractmethod

from pydantic import BaseModel

from typing import List, TYPE_CHECKING, Type

if TYPE_CHECKING:
    from wexample_filestate.options.abstract_option import AbstractOption
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractOptionsProvider(BaseModel, ABC):
    @abstractmethod
    def get_options(self) -> List[Type["AbstractOption"]]:
        pass

    @abstractmethod
    def get_operations(self) -> List[Type["AbstractOperation"]]:
        pass

from abc import ABC, abstractmethod
from typing import List, Type
from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractOperationsProvider(AbstractOptionsProvider, ABC):
    @abstractmethod
    def get_operations(self) -> List[Type["AbstractOperation"]]:
        pass

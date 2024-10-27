from abc import abstractmethod
from typing import TYPE_CHECKING, Type

from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractOperationTest(AbstractStateManagerTest):
    @abstractmethod
    def get_operation(self) -> Type["AbstractOperation"]:
        pass

    @abstractmethod
    def test_apply(self) -> None:
        pass
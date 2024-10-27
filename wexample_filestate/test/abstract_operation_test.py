import unittest
from abc import abstractmethod
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class AbstractOperationTest(unittest.TestCase):
    @abstractmethod
    def get_operation(self) -> Type["AbstractOperation"]:
        pass

    def setUp(self):
        pass

    @abstractmethod
    def test_apply(self) -> None:
        pass
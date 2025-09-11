from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@base_class
class AbstractOperationsProvider(BaseClass):
    @staticmethod
    def get_operations() -> list[type[AbstractOperation]]:
        return []

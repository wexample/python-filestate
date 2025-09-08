from __future__ import annotations

from typing import TYPE_CHECKING

import attrs
from wexample_helpers.classes.base_class import BaseClass

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


@attrs.define(kw_only=True)
class AbstractOperationsProvider(BaseClass):
    @staticmethod
    def get_operations() -> list[type[AbstractOperation]]:
        return []

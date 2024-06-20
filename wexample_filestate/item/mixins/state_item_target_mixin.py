from __future__ import annotations

from typing import cast, Optional

from wexample_filestate.helpers.operation_helper import operation_list_all
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin
from wexample_filestate.result.abstract_result import AbstractResult


class StateItemTargetMixin:
    _source: Optional[StateItemSourceMixin] = None

    @property
    def source(self):
        return self._source
    def configure(self, config: dict):
        if "name" in config:
            self._name = config["name"]

        if "mode" in config:
            self._mode = config["mode"]

    def build_operations(self, result: AbstractResult):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in operation_list_all():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target='self'))
from __future__ import annotations

from typing import cast, Optional, TYPE_CHECKING

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.operation_helper import operation_list_all
from wexample_filestate.item.mixins.state_item_source_mixin import StateItemSourceMixin
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class StateItemTargetMixin:
    _source: Optional[StateItemSourceMixin] = None

    @property
    def source(self):
        return self._source

    def __init__(self, state_manager: 'FileStateManager', path: FileStringOrPath,
                 config: Optional[StateItemConfig] = None):
        resolved_path = file_resolve_path(path)
        if resolved_path.is_file():
            from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
            self._source = FileStateItemFileSource(
                state_manager=state_manager,
                path=path)
        elif resolved_path.is_dir():
            from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
            self._source = FileStateItemDirectorySource(
                state_manager=state_manager,
                path=path)

        if config:
            self.configure(config)

    def configure(self, config: dict):
        if "name" in config:
            self._name = config["name"]

        if "mode" in config:
            self._mode = config["mode"]

    def build_operations(self, result: AbstractResult):
        from wexample_filestate.const.types_state_items import TargetFileOrDirectory

        for operation_class in operation_list_all():
            if operation_class.applicable(cast(TargetFileOrDirectory, self)):
                result.operations.append(operation_class(target=self))

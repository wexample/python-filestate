from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.enum.scopes import Scope


class YamlSortRecursiveOperation(FileManipulationOperationMixin, AbstractOperation):
    @classmethod
    def get_scope(cls) -> Scope:
        from wexample_filestate.enum.scopes import Scope

        return Scope.CONTENT

    @staticmethod
    def _is_sorted(data: Any) -> bool:
        """Return True if the current YAML content is already recursively key-sorted."""
        import yaml

        if not isinstance(data, str):
            return True

        try:
            data = yaml.safe_load(data)
        except Exception:
            # Unparseable, consider it not applicable for sorting
            return True

        def sort_rec(obj):
            if isinstance(obj, dict):
                return {k: sort_rec(obj[k]) for k in sorted(obj.keys())}
            if isinstance(obj, list):
                return [sort_rec(v) for v in obj]
            return obj

        sorted_data = sort_rec(data)
        current_dump = yaml.safe_dump(data, sort_keys=False)
        sorted_dump = yaml.safe_dump(sorted_data, sort_keys=False)
        return current_dump == sorted_dump

    def apply(self) -> None:
        import yaml

        data = self.target.get_local_file().read()
        if isinstance(data, str):
            data = yaml.safe_load(data)

        def sort_rec(obj):
            if isinstance(obj, dict):
                return {k: sort_rec(obj[k]) for k in sorted(obj.keys())}
            if isinstance(obj, list):
                return [sort_rec(v) for v in obj]
            return obj

        sorted_data = sort_rec(data)
        # Preserve a stable YAML dump
        dumped = yaml.safe_dump(sorted_data, sort_keys=False)

        self._target_file_write(content=dumped)

    def describe_after(self) -> str:
        return "The YAML file keys have been recursively sorted alphabetically."

    def describe_before(self) -> str:
        return "The YAML file may have unsorted keys; applying recursive alphabetical sort."

    def description(self) -> str:
        return "Sort YAML keys recursively in alphabetical order."

    def undo(self) -> None:
        self._restore_target_file()

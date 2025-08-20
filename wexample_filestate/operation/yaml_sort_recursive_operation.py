from __future__ import annotations

from typing import TYPE_CHECKING, Union, List, Type

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.enum.scopes import Scope
from wexample_filestate.operation.abstract_operation import AbstractOperation
from wexample_filestate.operation.mixin.file_manipulation_operation_mixin import (
    FileManipulationOperationMixin,
)

if TYPE_CHECKING:
    from wexample_filestate.item.item_target_directory import ItemTargetDirectory
    from wexample_filestate.item.item_target_file import ItemTargetFile


class YamlSortRecursiveOperation(FileManipulationOperationMixin, AbstractOperation):
    @classmethod
    def get_scope(cls) -> Scope:
        return Scope.NAME

    def dependencies(self) -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.file_create_operation import FileCreateOperation

        return [FileCreateOperation]

    @staticmethod
    def applicable_option(
            target: Union["ItemTargetDirectory", "ItemTargetFile"],
            option: "AbstractConfigOption",
    ) -> bool:
        from wexample_filestate.config_option.yaml_filter_config_option import (
            YamlFilterConfigOption,
        )

        if (
                target.is_file()
                and target.get_local_file().path.exists()
                and isinstance(option, YamlFilterConfigOption)
        ):
            value = option.get_value()
            if value is None:
                return False

            return value.has_item_in_list("sort_recursive")

        return False

    def description(self) -> str:
        return "Sort YAML keys recursively in alphabetical order."

    def describe_before(self) -> str:
        return "The YAML file may have unsorted keys; applying recursive alphabetical sort."

    def describe_after(self) -> str:
        return "The YAML file keys have been recursively sorted alphabetically."

    def apply(self) -> None:
        import yaml

        raw = self.target.get_local_file().read()
        data = yaml.safe_load(raw)

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

    def undo(self) -> None:
        self._restore_target_file()

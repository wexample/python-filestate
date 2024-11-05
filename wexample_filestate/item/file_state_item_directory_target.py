from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Type, Union, cast

from pydantic import Field
from wexample_config.const.types import DictConfig
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_helpers.const.types import FileStringOrPath
from wexample_prompt.io_manager import IOManager

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import (
        AbstractOptionsProvider,
    )
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
    from wexample_filestate.operations_provider.abstract_operations_provider import (
        AbstractOperationsProvider,
    )
    from wexample_filestate.result.abstract_result import AbstractResult
    from wexample_filestate.result.file_state_dry_run_result import (
        FileStateDryRunResult,
    )
    from wexample_filestate.result.file_state_result import FileStateResult


class FileStateItemDirectoryTarget(StateItemTargetMixin, FileStateItemDirectory):
    io: IOManager = Field(
        default_factory=IOManager,
        description="Handles output to print, allow to share it if defined in a parent context",
    )
    last_result: AbstractResult | None = None

    def __init__(self, config: DictConfig, **data):
        StateItemTargetMixin.__init__(self, config=config, **data)

    def configure_from_file(self, path: FileStringOrPath):
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read

        if yaml_read is not None:
            self.set_value(raw_value=yaml_read(str(path)))

    def get_children_list(self) -> list["TargetFileOrDirectoryType"]:
        from wexample_filestate.config_option.children_config_option import (
            ChildrenConfigOption,
        )

        option = cast(ChildrenConfigOption, self.get_option(ChildrenConfigOption))
        if option is not None:
            return option.get_children()

        return []

    def build_operations(self, result: "AbstractResult"):
        from wexample_filestate.const.types_state import TargetFileOrDirectory
        super().build_operations(result)


        for item in self.get_children_list():
            cast(TargetFileOrDirectory, item).build_operations(result)

    def find_by_name_recursive(self, name: str) -> Optional["TargetFileOrDirectoryType"]:
        found = self.find_by_name(name)
        if found:
            return found

        for child in self.get_children_list():
            if child.is_directory():
                result = cast(
                    FileStateItemDirectoryTarget, child
                ).find_by_name_recursive(name)
                if result:
                    return result

        return None

    def find_by_name(self, name: str) -> Optional["TargetFileOrDirectoryType"]:
        for child in self.get_children_list():
            if child.get_item_name() == name:
                return child

        return None

    def find_by_name_or_fail(self, name: str) -> "TargetFileOrDirectoryType":
        child = self.find_by_name(name)
        if child is None:
            from wexample_filestate.exception.item import ChildNotFoundException

            raise ChildNotFoundException(f"Child not found: {name}")

        return child

    def rollback(self) -> "FileStateResult":
        from wexample_filestate.result.file_state_result import FileStateResult

        result = FileStateResult(state_manager=self, rollback=True)

        # Fetch applied operations to a new stack.
        if self.last_result:
            for operation in self.last_result.operations:
                if operation.applied:
                    result.operations.append(operation)

        result.apply_operations()
        self.last_result = result

        return result

    def run(self, result: "AbstractResult") -> "AbstractResult":
        self.build_operations(result)
        self.last_result = result

        return self.last_result

    def dry_run(self) -> "FileStateDryRunResult":
        from wexample_filestate.result.file_state_dry_run_result import (
            FileStateDryRunResult,
        )

        return cast(
            FileStateDryRunResult, self.run(FileStateDryRunResult(state_manager=self))
        )

    def apply(self) -> "FileStateResult":
        from wexample_filestate.result.file_state_result import FileStateResult

        result = cast(FileStateResult, self.run(FileStateResult(state_manager=self)))
        result.apply_operations()

        return result

    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[DictConfig] = None,
        io: Optional[IOManager] = None,
        options_providers: Optional[List[Type["AbstractOptionsProvider"]]] = None,
        operations_providers: Optional[List[Type["AbstractOperationsProvider"]]] = None,
    ) -> "FileStateItemDirectoryTarget":
        import os

        from wexample_helpers.helpers.directory_helper import (
            directory_get_base_name,
            directory_get_parent_path,
        )

        config = config or {}

        # If path is a file, ignore file name a keep parent directory.
        if os.path.isfile(path):
            path = os.path.dirname(path)

        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
            io=io or IOManager(),
            options_providers=options_providers,
            operations_providers=operations_providers,
        )
